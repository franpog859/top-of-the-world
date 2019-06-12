import matplotlib.pyplot as plt
from numpy import *
import numpy as np
import rasterio
import rasterio.plot as plot
import nvector as nv

def get_geocoords_from_input(input_file):
    with rasterio.open(input_file) as src:
        #plot.show(src)
        elevation_values = src.read(1)
        lat_long_elev_data = []
        # Range is limited due to long execution time. for y in range(src.height):
        for y in range(50 * src.height // 100, 51 * src.height // 100): 
            # Range is limited due to long execution time. for x in range(src.width):
            for x in range(50 * src.width // 100, 51 * src.width // 100): 
                longitude, latitude = src.xy(x,y)
                elevation = elevation_values[x,y]
                lat_long_elev_data.append((
                    latitude, longitude, elevation
                ))
    return lat_long_elev_data


def geocoords_to_vectors(lat_long_elev_data):
    wgs84 = nv.FrameE(name='WGS84')
    vectors = []
    for latitude, longitude, elevation in lat_long_elev_data:
        pointB = wgs84.GeoPoint(
            latitude=latitude, longitude=longitude, z=elevation, degrees=True
        )
        p_EB_E = pointB.to_ecef_vector()
        x, y, z = p_EB_E.pvector.ravel()[0], p_EB_E.pvector.ravel()[1], p_EB_E.pvector.ravel()[2]
        vectors.append((
            latitude, longitude, x, y, z
        ))
    return vectors


def mark_tops_of_the_world(vectors):
    tops_of_the_world = []
    for examined_point in vectors:
        center = np.array([0,0,0])
        line_vector = np.array([examined_point[2], examined_point[3], examined_point[4]])

        points_on_line = []
        for point in vectors:
            point_on_line = closest_point_on_line(
                center, line_vector, np.array([point[2], point[3], point[4]])
            )
            x, y, z = point_on_line[0], point_on_line[1], point_on_line[2]
            points_on_line.append((
                point[0], point[1], x, y, z 
            ))

        top = max(points_on_line, key=distance)
        tops_of_the_world.append((top[0], top[1]))

    unique_tops = []
    for top in tops_of_the_world:
        if top not in unique_tops:
            unique_tops.append(top)

    return unique_tops


def closest_point_on_line(a, b, p):
    ap = p-a
    ab = b-a
    result = a + dot(ap,ab)/dot(ab,ab) * ab
    return result


def distance(point):
    return sqrt(point[2]**2 + point[3]**2 + point[4]**2)


def main():
    input_file = 'srtm_40_02.tif'

    print("Reading lat long elevation data from the {} file...".format(input_file))
    lat_long_elev_data = get_geocoords_from_input(input_file)

    print("Converting lat long elevation data to xyz vectors...")
    vectors = geocoords_to_vectors(lat_long_elev_data)

    print("Marking tops of the world...")
    tops_of_the_world = mark_tops_of_the_world(vectors)
    print(tops_of_the_world)
    
   
if __name__ == "__main__":
    main()
        