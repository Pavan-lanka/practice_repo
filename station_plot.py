from metpy.plots import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from metpy.units import units
import cv2 as cv

fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)

ax.set_title('Station Model')

# Define some sample data
temperature = 15.6
dewpoint = 10.2
wind_speed = 15
wind_direction = 0
pressure = 1010
cloud_height = 5
high_cloud = ''
mid_cloud = ''
low_cloud = ''
sky_covered = ''
visibility_distance = 0.5
present_weather = ''
past_weather = ''
press_tend = ''
press_change = '+'
pressure_difference = 15
precipitation = '.45'
sky_cover_at_lowest_cloud = 8
Station_ID = 'VOHS'
# Draw the station model
sp = StationPlot(ax, 0, 0, fontsize=13, spacing=25)
station_circle = patches.Circle((0, 0), radius=7, lw=1, edgecolor='k', facecolor='w')
# ax.set_aspect()
ax.add_patch(station_circle)

# to plot temperature in the model
sp.plot_text((-4, 3), text=[str(temperature) + '°C'], fontsize=13)

# to plot dew_point temperature in the model
sp.plot_text((-4, -3.5), text=[str(dewpoint) + '°C'], fontsize=13)

# to plot visibility distance in the model
sp.plot_text((-6, 0), text=[str(visibility_distance) + 'miles'], fontsize=13)

# adding a station plot to insert special figures
# sp.plot_barb([np.radians(wind_direction)], [wind_speed], length = 12)
# sp.plot_parameter('

# to position windbarb in the center of the model
# u = -wind_speed * np.sin(np.radians(wind_direction))
# v = -wspd_mps * math.cos(np.radians(wind_direction))
sp.plot_barb(u=[-wind_speed * np.sin(np.radians(wind_direction))],
             v=[-wind_speed * np.cos(np.radians(wind_direction))], length=10)

# to add wind speed in knots at the end of the barb
ax.text(1 * np.sin(np.radians(wind_direction)), 1 * np.cos(np.radians(wind_direction)),
        str(wind_speed) + ' kts', ha='center', va='bottom', rotation = 0, fontsize=10, alpha=0.3)

#to add Station ID to the model
sp.plot_text((8, 8), text=['Station_ID: '+ str(Station_ID)], fontsize=13)

# to add pressure to the model
sp.plot_text((4, 3), text=[str(pressure) + ' hPa'], fontsize=13)

# to add pressure_change to the model
sp.plot_text((3.2, 0), text=[str(press_change)], fontsize=13)

# to add pressure_difference to the model
sp.plot_text((4, 0), text=[str(pressure_difference)], fontsize=13)

# to add sky_cover_of the lowest cloud to the model
sp.plot_text((0, -3.7), text=[str(sky_cover_at_lowest_cloud)], fontsize=13)

# to add height of the cloud base
sp.plot_text((-2, -5.5), text=[str(cloud_height)], fontsize=13)

# to add precipitation to the model
sp.plot_text((2, -5.5), text=[str(precipitation)], fontsize=13)

# to add Sky_cover symbol to the model
sp.plot_symbol((0, 0), codes=[0], symbol_mapper=sky_cover, fontsize=25)

# to add pressure_tendency symbol to the model
sp.plot_symbol((5, 0), codes=[2], symbol_mapper=pressure_tendency, va='center', ha='center', fontsize=25)

# to add low_clouds symbol to the model
sp.plot_symbol((-2, -3.5), codes=[1], symbol_mapper=low_clouds, va='center', ha='center', fontsize=25)

# to add mid_clouds symbol to the model
sp.plot_symbol((2, 3), codes=[8], symbol_mapper=mid_clouds, va='center', ha='center', fontsize=25)

# to add high_clouds symbol to the model
sp.plot_symbol((1, 5), codes=[1], symbol_mapper=high_clouds, va='center', ha='center', fontsize=25)

# to add current_weather symbol to the model
sp.plot_symbol((-4, 0), codes = [wx_code_map['TS']], symbol_mapper=current_weather, va='center', ha='center', fontsize=25)

# to add past_weather symbol to the model
sp.plot_symbol((2, -3.5), codes=[wx_code_map['TS']], symbol_mapper=current_weather, va='center', ha='center', fontsize=25)

# adding metpy logo at the corner
# al = add_metpy_logo(fig=fig, x=8, y=8, zorder=5, size='small')

# plt.grid()
# plt.show()
path = '/home/hp/PycharmProjects/station_model/'
name = 'Station_Model.jpeg'
plt.savefig(path+name, dpi= 100)
cv.waitKey(5)
print(wx_code_map['TS'])
image = cv.imread(path+name)
cv.imshow(name.rstrip('.jpeg'), image)
k = cv.waitKey(0) & 0xFF
print(k)
if k == 233 :  # close on ESC key
    cv.destroyAllWindows()

