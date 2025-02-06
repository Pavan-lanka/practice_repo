#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:18:29 2024

@author: ubuntu
"""

from pyproj import Transformer
from astropy import units as u
from astropy.coordinates import EarthLocation, AltAz, get_sun
from astropy.time import Time
import numpy as np
import pytz
from datetime import datetime
import pandas as pd
import time
import rasterio
import os
from typing import List, Tuple, Dict, Optional

# Configurations
MAXIMUM_VISIBILITY = 250
SUCCESSIVE_DISTANCE = 105

# Column Mappings
GROUND_TRACES_COLUMNS = {'epoch_time': 'Epoch_Time', 'lat': 'Latitude', 'lon': 'Longitude'}
TARGETS_COLUMNS = {'id': 'id', 'name': 'location_name', 'lat': 'latitude', 'lon': 'longitude'}
FINAL_RESULT_COLUMNS = {
    'epoch_time': 'Epoch_Time', 'time(UTC)': 'Time(UTC)', 'lat': 'Latitude(sat)',
    'lon': 'Longitude(sat)', 'distance': 'distance(km)', 'cloud': 'cloud(%)'
}

# Cloud cover functions


def find_closest_time(tif_dic, input_time):
    return min(tif_dic.keys(), key=lambda t: abs(t - input_time))


def find_cloud_present(dataset, lat, lon):
    if dataset.crs.to_string() != 'EPSG:4326':
        lon, lat = Transformer.from_crs("EPSG:4326", dataset.crs, always_xy=True).transform(lon, lat)
    row, col = dataset.index(lon, lat)
    return dataset.read(4)[row, col] / 2


def get_cloud(tifs_dict, lat, lon, imaging_utc):
    closest_tif_key = find_closest_time(tifs_dict, imaging_utc)
    return find_cloud_present(tifs_dict[closest_tif_key], lat, lon)

# Day/Night calculation


def is_day_or_night(lat, lon, epoch_time):
    location = EarthLocation.from_geodetic(lon, lat)
    utc_time = Time(epoch_time, format='unix')
    sun_altaz = get_sun(utc_time).transform_to(AltAz(obstime=utc_time, location=location))
    return sun_altaz.alt > 0 * u.deg

# Satellite data interpolation


def interpolate_satellite_data_numpy(data):
    if len(data) <= 1:
        return data

    interpolated_segments = []
    for i in range(len(data) - 1):
        start, end = data[i, 0], data[i + 1, 0]
        num_seconds = int(end - start)
        time_range = np.arange(start, end + 1)
        latitudes = np.linspace(data[i, 1], data[i + 1, 1], num_seconds + 1)
        longitudes = np.linspace(data[i, 2], data[i + 1, 2], num_seconds + 1)
        segment = np.column_stack((time_range, latitudes, longitudes))
        if i < len(data) - 2:  # Avoid duplicate rows
            segment = segment[:-1]
        interpolated_segments.append(segment)
    return np.vstack(interpolated_segments)

# Haversine distance calculation


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def find_closest_row(trace, target):
    distances = np.array([haversine(target[0], target[1], lat, lon) for lat, lon in trace[:, 1:3]])
    closest_index = np.argmin(distances)
    return closest_index, distances[closest_index]

# Data loaders


def load_targets(targets_path: str) -> pd.DataFrame:
    return pd.read_excel(targets_path)


def load_ground_traces(groundtraces_path: str) -> List[Tuple[str, np.ndarray]]:
    ground_traces = []
    for file_name in os.listdir(groundtraces_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(groundtraces_path, file_name)
            df = pd.read_csv(file_path)
            np_array = df[[GROUND_TRACES_COLUMNS['epoch_time'], GROUND_TRACES_COLUMNS['lat'], GROUND_TRACES_COLUMNS['lon']]].to_numpy()
            ground_traces.append((file_name, np_array))
    return ground_traces


def load_geotiffs_to_dict(cloud_cover_path: str) -> Dict:
    tiff_dict = {}
    for filename in os.listdir(cloud_cover_path):
        if filename.endswith((".tif", ".tiff")):
            file_path = os.path.join(cloud_cover_path, filename)
            tiff_dict[filename_to_epoch_utc(filename)] = rasterio.open(file_path)
    return tiff_dict


def filename_to_epoch_utc(filename):
    _, time_part = filename.split("_f")
    dt = pytz.UTC.localize(datetime.strptime(time_part.split(".")[0], "%Y%m%d-%H"))
    return int(dt.timestamp())

# Data enrichment


# def enrich_imaging_data(target_df, result_dict, cloudcover_tifs_dict):
#     target_mapping = {(row[TARGETS_COLUMNS['lat']], row[TARGETS_COLUMNS['lon']]): row[TARGETS_COLUMNS['name']] for _, row in target_df.iterrows()}
#     updated_result_dict = {}
#     for key, arr in result_dict.items():
#         if isinstance(arr, np.ndarray) and arr.shape[1] == 4:
#             # lat, lon = key
#             idx, lat, lon = key
#             enriched_rows = [
#                 [row[0], datetime.utcfromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S'), lat, lon, row[3],
#                  get_cloud(cloudcover_tifs_dict, lat, lon, row[0])]
#                 for row in arr if is_day_or_night(lat, lon, row[0])
#             ]
#             updated_result_dict[(target_mapping.get((lat, lon), "Unknown"), lat, lon)] = pd.DataFrame(
#                 enriched_rows, columns=FINAL_RESULT_COLUMNS.values())
#     return updated_result_dict
def enrich_imaging_data(target_df, result_dict, cloudcover_tifs_dict):
    target_mapping = {(row[TARGETS_COLUMNS['lat']], row[TARGETS_COLUMNS['lon']]): row[TARGETS_COLUMNS['id']] for _, row in target_df.iterrows()}

    updated_result_dict = {}
    for key, arr in result_dict.items():
        if isinstance(arr, np.ndarray) and arr.shape[1] == 4:
            lat, lon = key
            enriched_pairs = [
                (row[0], get_cloud(cloudcover_tifs_dict, lat, lon, row[0]))
                for row in arr if is_day_or_night(lat, lon, row[0])
            ]
            id = target_mapping.get((lat, lon), "Unknown")
            updated_result_dict[id] = enriched_pairs

    return updated_result_dict


# Main processing function
def find_imaging_time_with_cloud_coverage(targets_df, targets_np_array, ground_traces, cloudcover_tifs_dict):
    result_dict = {}
    # for __lat, __lon in targets_np_array:
    for idx, (__lat, __lon) in enumerate(targets_np_array):
        _temp_list_of_arr = np.empty((0, 4))
        for _, trace in ground_traces:
            visibility_cushion = MAXIMUM_VISIBILITY + SUCCESSIVE_DISTANCE
            closest_index, closest_distance = find_closest_row(trace, (__lat, __lon))
            if closest_distance <= MAXIMUM_VISIBILITY:
                _temp_list_of_arr = np.append(_temp_list_of_arr, [np.append(trace[closest_index], closest_distance)], axis=0)
            elif closest_distance <= visibility_cushion:
                interp_data = interpolate_satellite_data_numpy(trace[max(0, closest_index - 1):min(len(trace), closest_index + 2)])
                closest_index, closest_distance = find_closest_row(interp_data, (__lat, __lon))
                if closest_distance <= MAXIMUM_VISIBILITY:
                    _temp_list_of_arr = np.append(_temp_list_of_arr, [np.append(trace[closest_index], closest_distance)], axis=0)
        result_dict[(__lat, __lon)] = _temp_list_of_arr
    return enrich_imaging_data(targets_df, result_dict, cloudcover_tifs_dict)

# Main execution


def main():
    # File Paths
    TARGETS_PATH = '/home/pavan_azista/Documents/bd_targets.ods'
    GROUND_TRACES_PATH = '/home/pavan_azista/static/media/trajectory'
    CLOUD_COVER_PATH = '/home/pavan_azista/static/media/cloud_forecast'

    targets_df = load_targets(TARGETS_PATH)
    targets_np_array = targets_df[[TARGETS_COLUMNS['lat'], TARGETS_COLUMNS['lon']]].to_numpy()

    ground_traces = load_ground_traces(GROUND_TRACES_PATH)
    cloudcover_tifs_dict = load_geotiffs_to_dict(CLOUD_COVER_PATH)

    start_time = time.time()
    final_result = find_imaging_time_with_cloud_coverage(targets_df, targets_np_array, ground_traces, cloudcover_tifs_dict)
    print(f"Processing complete in {time.time() - start_time:.2f} seconds")

    return final_result


if __name__ == '__main__':
    result = main()
    print(result)
