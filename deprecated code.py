from datetime import datetime
import matplotlib.pyplot as plt
import datetime
import numpy as np
from meteostat import Hourly
# Set time period
start = datetime.datetime(2018, 1, 1)
end = datetime.datetime(2018, 12, 31, 23, 59)
data = Hourly('43125' ,start, end)
data1 = Hourly('43133' ,start, end)
data = data.fetch()
data1 = data1.fetch()
station_of_interest = data.iloc[:,0].to_frame().reset_index()
neigh = data1.iloc[:, 0].to_frame().reset_index()
station_of_interest.rename(columns={'time': 'date_time'},inplace = True)
neigh.rename(columns={'time': 'date_time'},inplace = True)



# Example data
dates = [datetime.datetime(2023, 3, i) for i in range(1, 6)]
station1_temps = [36, 37, 37, 38, 35]
station2_temps = [36, 37, 39, 21, 35]

# Calculate linear regression
x = [date.timestamp() for date in dates]
y1 = station1_temps
y2 = station2_temps
mean_x = sum(x) / len(x)
mean_y1 = sum(y1) / len(y1)
mean_y2 = sum(y2) / len(y2)
numerator1 = sum([(x[i] - mean_x) * (y1[i] - mean_y1) for i in range(len(x))])
denominator1 = sum([(x[i] - mean_x) ** 2 for i in range(len(x))])
slope1 = numerator1 / denominator1
intercept1 = mean_y1 - slope1 * mean_x
numerator2 = sum([(x[i] - mean_x) * (y2[i] - mean_y2) for i in range(len(x))])
denominator2 = sum([(x[i] - mean_x) ** 2 for i in range(len(x))])
slope2 = numerator2 / denominator2
intercept2 = mean_y2 - slope2 * mean_x

# Plot data and regression lines
plt.plot(dates, y1, 'o', label='Station 1')
plt.plot(dates, [slope1 * xi + intercept1 for xi in x], '-', label='Station 1 Regression')
plt.plot(dates, y2, 'o', label='Station 2')
plt.plot(dates, [slope2 * xi + intercept2 for xi in x], '-', label='Station 2 Regression')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title('Temperature of Two Stations over Time')
plt.legend()
plt.show()


'''
Custom_file_Read
if self.path_to_file[-4:] == '.csv':
        data = pd.read_csv(self.path_to_file)
        d_parameters = list(data.columns.values)
        return data, d_parameters
    elif '.txt' in self.path_to_file[-4:]:
        data = parse_metar_file(filename=self.path_to_file)
        d_parameters = list(data.columns.values)
        return data, d_parameters
    elif self.path_to_file[-4:] == '.xml':
        data = pd.read_xml(path_or_buffer=self.path_to_file)
        d_parameters = list(data.columns.values)
        return data, d_parameters
    elif self.path_to_file[-3:] == '.nc':
        data = xr.open_dataset(filename_or_obj=self.path_to_file, engine="netcdf4")
        data = data.metpy.parse_cf()
        data = data.to_dataframe()
        data = data.reset_index()
        d_parameters = list(data.columns.values)
        return data, d_parameters
    elif not self.path_to_file[-4:] in ['.txt', '.nc', '.xml', '.csv']:
        raise RuntimeError ('File Format should be a .csv, .txt, .cn or .xml file')
'''
'''        
fetch_station_data
        # if obs_frequency.lower() == 'hourly':
        #     if start_time >= end_time:
        #         print('Enter Valid date time to fetch hourly data')
        #     else:
        #         data = mt.Hourly(self.station_id, start_time, end_time)
        #         data = data.fetch()
        #         d_parameters = list(data.columns.values)
        #         return data, d_parameters
        # elif obs_frequency.lower() == 'daily':
        #     if start_time >= end_time:
        #         print('Enter Valid days for fetching Daily data')
        #     else:
        #         data = mt.Daily(self.station_id, start_time, end_time)
        #         data = data.fetch()
        #         d_parameters = list(data.columns.values)
        #         return data, d_parameters
        # elif obs_frequency.lower() == 'monthly':
        #     if start_time >= end_time:
        #         print('Enter Valid months in Date,Time for fetching monthly data')
        #     else:
        #         data = mt.Monthly(self.station_id, start_time, end_time)
        #         data = data.fetch()
        #         d_parameters = list(data.columns.values)
        #         return data, d_parameters
        # else:
        #     return print('The data period frequency is not valid')
'''