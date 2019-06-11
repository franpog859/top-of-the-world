import matplotlib.pyplot as plt
import rasterio
from rasterio import plot

input_file = 'srtm_40_02.tif'

def get_input_data(src):
    elevation_values = src.read(1)
    data = []
    for y in range(50 * src.height // 100, 51 * src.height // 100): # Range is limited due to long execution time. for y in range(src.height):
        for x in range(50 * src.width // 100, 51 * src.width // 100): # Range is limited due to long execution time. for x in range(src.width):
            width, height = src.xy(x,y)
            elevation = elevation_values[x,y]
            data.append((
                width, height, elevation
            ))
    return data


with rasterio.open(input_file) as src:
    plot.show(src)

    data = get_input_data(src)
    print(data[-1])
