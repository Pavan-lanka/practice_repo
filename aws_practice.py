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