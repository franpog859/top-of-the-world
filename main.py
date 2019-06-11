import matplotlib.pyplot as plt
import rasterio
import rasterio.plot as plot
import nvector as nv

def get_input_data(src):
    elevation_values = src.read(1)
    lat_long_elev_data = []
    for y in range(50 * src.height // 100, 51 * src.height // 100): # Range is limited due to long execution time. for y in range(src.height):
        for x in range(50 * src.width // 100, 51 * src.width // 100): # Range is limited due to long execution time. for x in range(src.width):
            longitude, latitude = src.xy(x,y)
            elevation = elevation_values[x,y]
            lat_long_elev_data.append((
                latitude, longitude, elevation
            ))
    return lat_long_elev_data


input_file = 'srtm_40_02.tif'
with rasterio.open(input_file) as src:
    #plot.show(src)
    lat_long_elev_data = get_input_data(src)

print(lat_long_elev_data[-1])
wgs84 = nv.FrameE(name='WGS84')
pointB = wgs84.GeoPoint(latitude=lat_long_elev_data[0][0], longitude=lat_long_elev_data[0][1], z=lat_long_elev_data[0][2], degrees=True)
p_EB_E = pointB.to_ecef_vector()
print(p_EB_E.pvector.ravel())


