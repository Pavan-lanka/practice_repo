from metpy.plots import *
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from metpy.io import *
import pandas as pd
import meteostat as mt
from datetime import datetime as dt
from dataclasses import dataclass
import metpy


@dataclass
class StationModelPlot:
    station_id: str = ''
    path_to_file: str = ''

    '''StationModelPlot Class takes Station_ID as String. ex:'12992'
    
    '''

    def fetch_station_data(self, start_time: dt, end_time: dt, obs_frequency='hourly'):
        """ start is Start time for accumulation of observations in dt format. ex_Input: dt(YYYY, MM, DD, HH, MM, SS)
        end is End time range of the accumulation of data in dt format . dt(YYYY, MM, DD, HH, MM, SS)
                                                                        -> (2022,  1,  2, 23, 59)
        obs_frequency is observations frequency. parameter accepts string, defaults to 'Hourly'
        Ex. 'Monthly','Daily'
        Example input:
        # a = StationModelPlot('43128')
        # a = a.fetch_station_data(dt(2022, 1, 1), dt(2022, 1, 1, 23, 59), 'hourly')"""
        frequency = ['hourly', 'daily', 'monthly']
        frequency_fetch = {'hourly' : mt.Hourly,
                           'monthly' : mt.Monthly,
                           'daily' : mt.Daily

        }
        if obs_frequency.lower() in frequency and start_time <= end_time:
            data = frequency_fetch[obs_frequency](self.station_id, start_time, end_time)
            data = data.fetch()
            data = data.reset_index()
            d_parameters = list(data.columns.values)
            return data, d_parameters
        elif obs_frequency.lower() not in frequency:
            raise RuntimeError(f'Enter a valid observation frequency from {frequency}')
        else:
            raise RuntimeError ('Start time should be less than End time')



    def custom_file_read(self):
        """This method takes the file as object or File_Path as input parameter and returns DF from
        # a= CustomData('pa1.csv')
        # a = a.custom_file_read()
        # print(a)
        """
        supported_types = ['nc', 'xml', 'txt', 'csv']
        extension_read = {'nc' : xr.open_dataset,
                          'xml' : pd.read_xml,
                          'txt' : parse_metar_file,
                          'csv' : pd.read_csv
        }
        extension = self.path_to_file[self.path_to_file.rfind('.'):][1:]
        if extension not in supported_types:
            raise RuntimeError(f'Supported file formats are {supported_types}')
        elif extension == 'nc':
            data = extension_read['nc'](self.path_to_file, engine="netcdf4")
            data = data.metpy.parse_cf()
            data = data.to_dataframe()
            data = data.reset_index()
        else:
            data = extension_read[extension](self.path_to_file)
        d_parameters = list(data.columns.values)
        return data, d_parameters

    @staticmethod
    def get_input_data(self):
        ts_str = input("Enter a timestamp in the format 'YYYY-MM-DD HH:MM:SS': ")
        ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
        return ts

    @staticmethod
    def param_data_validation(self):
        a, b = StationModelPlot.custom_file_read(self)
        ip = StationModelPlot.get_input_data(self)
        parameter_abbreviations = {
            'station_id':['Station_ID','station', 'station_id' ],
            'date_time': ['valid', 'time', 'date_time', 'time1', 'time_stamp', 'DATE_TIME'],

            'temperature': ['Temperature', 'TEMPERATURE', 'tmpt', 'air_temperature',
                            'temp', 'tmpf', 'tmpc', 'temperature', 'tavg'],
            'dew_point_temperature': ['Dew_Point_Temperature', 'DEW_POINT_TEMPERATURE', 'dwpt', 'dwpc',
                                      'dew_temp', 'dwpf', 'dew_point_temperature'],
            'wind_speed': ['WIND_SPEED', 'wspd', 'sknt', 'Wind_Speed', 'wind_speed'],
            'wind_direction': ['WIND_DIRECTION', 'Wind_Direction', 'drct', 'wdir', 'wind_direction'],
            'cloud_height': ['skyl3', 'highest_cloud_level', 'high_cloud_level',
                             'medium_cloud_level', 'low_cloud_level'],
            'pressure': ['PRESSURE', 'pres', 'mslp', 'atmospheric_pressure', 'air_pressure_at_sea_level'],
            'high_cloud': ['high_cloud_type', 'skyc3', 'high_cloud'],
            'mid_cloud': ['mid_cloud_type', 'skyc2', 'mid_cloud'],
            'low_cloud': ['low_cloud_type', 'skyc1','low_cloud'],
            'sky_cover': ['cloud_coverage', 'skyc1','sky_cover'],
            'visibility_distance': ['visibility', 'vsby','visibility_distance'],
            'present_weather': ['coco', 'current_weather', 'wxcodes', 'current_wx1','present_weather'],
            'past_weather': None,
            'pressure_tendency': None,
            'pressure_change': None,
            'pressure_difference': None,
            'precipitation': ['p01i', 'prcp', 'PRECIPITATION', 'precipitation'],
            'sky_cover_at_lowest_cloud': ['low_cloud_level', 'skyl1',
                                          'SKY_COVER_AT_LOWEST_CLOUD', 'sky_cover_at_lowest_cloud']
        }
        data_to_plot = {

        }
        # for i in range(len(b)):
        #     if b[i] in parameter_abbreviations['date_time']:
        #         if ip in a[b[i]]:
        #             c = a.loc[a[b[i]] == ip]
        #             c = c.squeeze()
        #             data_to_plot = c.to_dict()
        #         else:
        #             print(f"Entered TimeStamp doesn't exist in the {self.path}")
        # 
        #     else:
        #         for key, val in parameter_abbreviations:
        #             if b[i] in parameter_abbreviations:
        #                 data_to_plot[b[i]] = a.
        #             elif b[i] not in parameter_abbreviations:
        #                 for j in val:
        return a




# a = FetchData(path_to_file=r"C:\Users\Pavan Koundinya\Desktop\metar_vij.txt")
# a, b = a.custom_file_read()
# an = list(a.columns.values)
# print(an)


@dataclass()
class StationModel(StationModelPlot):
    fig, ax = plt.subplots(figsize=(10, 10))
    sp = StationPlot(ax, 0, 0, fontsize=13, spacing=25)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_title('Station Model')
    station_circle = patches.Circle((0, 0), radius=7, lw=1, edgecolor='k', facecolor='w')
    ax.add_patch(station_circle)
    data = {
        # 'temperature': None,
        # 'dew_point_temperature': None,
        # 'wind_speed': None,
        # 'wind_direction': None,
        # 'cloud_height': None,
        # 'pressure': None,
        # 'high_cloud': None,
        # 'mid_cloud': None,
        # 'low_cloud': None,
        # 'sky_cover': None,
        # 'visibility_distance': None,
        # 'present_weather': None,
        # 'past_weather': None,
        # 'pressure_tendency': None,
        # 'pressure_change': None,
        # 'pressure_difference': None,
        # 'precipitation': None,
        # 'sky_cover_at_lowest_cloud': None
    }

    def plot_station_model(self):


        # to add pressure_tendency symbol to the model
        self.sp.plot_symbol((5, 0), codes=[self.data['pressure_tendency']], symbol_mapper=pressure_tendency,
                            va='center', ha='center', fontsize=25)

        # to add Sky_cover symbol to the model
        self.sp.plot_symbol((0, 0), codes=[self.data['sky_cover']], symbol_mapper=sky_cover, fontsize=25)

        # to add pressure to the model
        self.sp.plot_text((4, 3), text=[str(self.data['pressure']) + ' hPa'], fontsize=13)

        # to position wind-barb in the center of the model
        # u = -wind_speed * np.sin(np.radians(wind_direction))
        # v = -wspd_mps * math.cos(np.radians(wind_direction))
        self.sp.plot_barb(u=[-(self.data['wind_speed']) * np.sin(np.radians(self.data['wind_direction']))],
                          v=[-(self.data['wind_speed']) * np.cos(np.radians(self.data['wind_direction']))], length=11)
        # to add wind speed in knots at the end of the barb
        self.ax.text(1.5 * np.sin(np.radians(self.data['wind_direction'])),
                     1.5 * np.cos(np.radians(self.data['wind_direction'])),
                     str(self.data['wind_speed']) + ' kts',
                     ha='center', va='bottom', rotation=0, fontsize=10, alpha=0.3)

        # to add height of the cloud base
        self.sp.plot_text((-2, -5.5), text=[str(self.data['cloud_height'])], fontsize=13)

        # to add dew_point_temperature to the model
        self.sp.plot_text((-4, 3), text=[str(self.data['dew_point_temperature']) + '°C'], fontsize=13)

        # to add high_clouds symbol to the model
        self.sp.plot_symbol((1, 5), codes=[self.data['high_cloud']], symbol_mapper=high_clouds,
                            va='center', ha='center', fontsize=25)

        # to add low_clouds symbol to the model
        self.sp.plot_symbol((-2, -3.5), codes=[self.data['low_cloud']], symbol_mapper=low_clouds,
                            va='center', ha='center', fontsize=25)

        # to add mid_clouds symbol to the model
        self.sp.plot_symbol((2, 3), codes=[self.data['mid_cloud']], symbol_mapper=mid_clouds,
                            va='center', ha='center', fontsize=25)

        # to add past_weather symbol to the model
        self.sp.plot_symbol((2, -3.5), codes=wx_code_map[self.data['past_weather']], symbol_mapper=current_weather,
                            va='center', ha='center', fontsize=25)

        # to add precipitation to the model
        self.sp.plot_text((2, -5.5), text=[str(self.data['precipitation'])], fontsize=13)

        # to add present_weather symbol to the model
        self.sp.plot_symbol((-4, 0), codes=wx_code_map[self.data['present_weather']], symbol_mapper=current_weather,
                            va='center', ha='center', fontsize=25)

        # to add pressure_change to the model
        self.sp.plot_text((3.2, 0), text=[str(self.data['pressure_change'])], fontsize=13)

        # to add pressure_difference to the model
        self.sp.plot_text((4, 0), text=[str(self.data['pressure_difference'])], fontsize=13)

        # to add sky_cover_of the lowest cloud to the model
        self.sp.plot_text((0, -4), text=[str(self.data['sky_cover_at_lowest_cloud'])], fontsize=13)

        # to add temperature to the model
        self.sp.plot_text((-4, 3), text=[str(self.data['temperature']) + '°C'], fontsize=13)

        # to add visibility_distance to the model
        self.sp.plot_text((-6, 0), text=[str(self.data['visibility_distance']) + 'miles'], fontsize=13)
        return plt.show()




# adding metpy logo at the corner
# al = add_metpy_logo(fig=fig, x=8, y=8, zorder=5, size='small')

# plt.grid()
a =  StationModelPlot("")