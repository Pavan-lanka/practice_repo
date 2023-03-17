from metpy.plots import sky_cover, high_clouds
from metpy.units import units
import metpy.plots as plots
import matplotlib.pyplot as plt

# # Set up the plot and axis
# fig, ax = plt.subplots(figsize=(6, 6))
# ax.set_xlim(1, 10)
# ax.set_ylim(1, 10)
#
# # Create the station model plot
# stationplot = plots.StationPlot(ax, 0, 0, fontsize=14)
#
# # Add a title to the plot
# plt.title('Station Model Example')
#
# # Show the plot
# plt.show() '''
# import metpy.plots as plots
# from metpy.units import units
# import matplotlib.pyplot as plt
# import datetime
# import meteostat as mt
# start = datetime.datetime(2018, 1, 1)
# end = datetime.datetime(2018, 12, 31, 23, 59)
# data = mt.Hourly('43125', start, end)
# data1 = mt.Hourly('43133', start, end)
# data = data.fetch()
# data1 = data1.fetch()
# # Setting up the plot and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
#
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
# station_model.plot_barb(wind_dir, wind_speed)
# station_model.plot_parameter('NW', temp)
# station_model.plot_parameter('SW', dewpt)

# station_model.plot_symbol(location=(-0.3, 0), codes=[('VA',5)], symbol_mapper=sky_cover)


# station_model.plot_symbol(cloud_cover, symbol_mapper=5)
# station_model.plot_text((0, -0.4), f'{pressure.magnitude:.0f}', fontsize=16, ha='center')
#
# Add a title to the plot

if symbol1 == '1_hs':
    station_model.plot_symbol(location=(-0.3, 0), codes=[1], symbol_mapper=high_clouds)
if symbol1 == '2_hs':
    station_model.plot_symbol(location=(-0.3, 0), codes=[2], symbol_mapper=high_clouds)
if symbol1 == '3_hs':
    station_model.plot_symbol(location=(-0.3, 0), codes=[3], symbol_mapper=high_clouds)
if symbol1 == '4_hs':
    station_model.plot_symbol(location=(-0.3, 0), codes=[4], symbol_mapper=high_clouds)
if symbol1 == '5_hs':
    station_model.plot_symbol(location=(-0.3, 0), codes=[5], symbol_mapper=high_clouds)
if symbol1 == '6_hs':
    station_model.plot_symbol(location=(-0.3, 0), codes=[6], symbol_mapper=high_clouds)


if  symbol1[-3:]=='_hs':
     station_model.plot_symbol(location=(-0.3, 0), codes=[int(symbol1[:1])], symbol_mapper=high_clouds)

if symbol1 == '1_hs':
    station_model.plot_symbol(location=(-0.3, 0), codes=[1], symbol_mapper=high_clouds)

plt.title('Weather Station Model')

# Show the plot
plt.show()
# import cv2
# import tesseract
#
# # setting the path of pytesseract exe
# # you have to write the location of
# # on which your tesseract was installed
# tesseract.tesseract_cmd = '/home/hp/Desktop/tesseract-ocr-0.0.1/bin'
#
# # Now we will read the image in our program
# # you have to put your image path in place of photo.jpg
# img = cv2.imread('skycover.png')
#
# # Our image will read as BGR format,
# # So we will convert in RGB format because
# # tesseract can only read in RGB format
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
# # For getting the text and number from image
# print(tesseract.image_to_string(img))
#
# # For displaying the original image
# cv2.imshow("result", img)
# cv2.waitKey(0)