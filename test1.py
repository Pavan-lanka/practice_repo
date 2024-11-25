import matplotlib.pyplot as plt
from metpy.calc import reduce_point_density
from metpy.cbook import get_test_data
from metpy.io import metar
from metpy.plots import add_metpy_logo, current_weather, sky_cover, StationPlot

data = metar.parse_metar_file(get_test_data('metar_20190701_1200.txt', as_file_obj=False))
data = data.dropna(how='any', subset=['wind_direction', 'wind_speed'])
parameters = list(data.columns.values)
print(parameters)
