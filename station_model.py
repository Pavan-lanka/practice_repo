import metpy.plots as plots
from metpy.units import units
import matplotlib.pyplot as plt
import pandas as pd
import meteostat as mt
from datetime import datetime as dt


class FetchData:
    # __init__ takes Station ID of the required Station Model
    def __init__(self, station_id: str , start : dt, end : dt, period:str ):
        self.station_id = station_id
        self.start = start
        self.end = end
        self.period = period

    def fetch_station_data(self):
        """ to get Station data
            start = datetime(starting time period of the required data) ex. datetime(
            end = ending time period of the required data
            period = Frequency of the data period i.e(Hourly, Monthly, Daily)"""
        if self.period.lower() == 'hourly':
            if self.start > self.end:
                print('Enter Valid hours as you provided same start date time and end date time')
            else:
                data = mt.Hourly(self.station_id, self.start, self.end)
                data = data.fetch()
                return data
        elif self.period.lower() == 'daily':
            if self.start > self.end or self.start == self.end:
                print('Enter Valid days for getting Daily data')
            else:
                data = mt.Daily(self.station_id, self.start, self.end)
                data = data.fetch()
                return data
        elif self.period.lower() == 'monthly':
            if self.start > self.end or self.start == self.end:
                print('Enter Valid months in Date,Time for fetching monthly data')
            else:
                data = mt.Monthly(self.station_id, self.start, self.end)
                data = data.fetch()
                return data
        else:
            return print('The data period frequency is not valid')

class CustomData:
    def path_to_file(self,PATH_TO_FILE):
        self.PATH_TO_FILE = PATH_TO_FILE
