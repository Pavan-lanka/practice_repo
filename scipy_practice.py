'''import metpy.plots as plots
import matplotlib.pyplot as plt

# Set up the plot and axis
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(1, 10)
ax.set_ylim(1, 10)

# Create the station model plot
stationplot = plots.StationPlot(ax, 0, 0, fontsize=14)

# Add a title to the plot
plt.title('Station Model Example')

# Show the plot
plt.show() '''
import metpy.plots as plots
from metpy.units import units
import matplotlib.pyplot as plt
import datetime
import meteostat as mtclass 
start = datetime.datetime(2018, 1, 1)
end = datetime.datetime(2018, 12, 31, 23, 59)
data = mt.Hourly('43125', start, end)
data1 = mt.Hourly('43133', start, end)
data = data.fetch()
data1 = data1.fetch()
# Setting up the plot and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)

#Defining the weather variables
temp = [72.0] * units.degF
dewpt = [54.0] * units.degF
wind_speed = [10.0] * units.knots
wind_dir = [180.0] * units.degrees
cloud_cover = [50.0] * units.percent
present_weather = 'RA'
pressure = 1005.0 * units.hPa

# Create the station model plot
station_model = plots.StationPlot(ax, 0, 0, fontsize=12)

# Add the weather variables to the plot
station_model.plot_barb(wind_dir, wind_speed)
station_model.plot_parameter('NW', temp)
station_model.plot_parameter('SW', dewpt)
station_model.plot_symbol(location=(-0.3, 0), codes=present_weather, symbol_mapper=5)
station_model.plot_symbol(cloud_cover, symbol_mapper=5)
station_model.plot_text((0, -0.4), f'{pressure.magnitude:.0f}', fontsize=16, ha='center')

# Add a title to the plot

plt.title('Weather Station Model')

# Show the plot
plt.show()