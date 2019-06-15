import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.plot as plot
import nvector as nv
from tqdm import tqdm


def get_geocoords_from_input(input_file):
    with rasterio.open(input_file) as src:
        #plot.show(src)
        elevation_values = src.read(1)
        lat_long_elev_data = []
        # Range is limited due to long execution time. for y in range(src.height):
        for y in range(0, src.height, 100): 
            # Range is limited due to long execution time. for x in range(src.width):
            for x in range(0, src.width, 100): 
                longitude, latitude = src.xy(x,y)
                elevation = elevation_values[x,y]
                lat_long_elev_data.append((
                    x, y, latitude, longitude, elevation
                ))
    return lat_long_elev_data


def geocoords_to_vectors(lat_long_elev_data):
    wgs84 = nv.FrameE(name='WGS84')
    vectors = []
    for width, height, latitude, longitude, elevation in lat_long_elev_data:
        pointB = wgs84.GeoPoint(
            latitude=latitude, longitude=longitude, z=elevation, degrees=True
        )
        p_EB_E = pointB.to_ecef_vector()
        x, y, z = p_EB_E.pvector.ravel()[0], p_EB_E.pvector.ravel()[1], p_EB_E.pvector.ravel()[2]
        vectors.append((
            width, height, latitude, longitude, x, y, z
        ))
    return vectors


def mark_tops_of_the_world(vectors):
    tops_of_the_world = []
    pbar = tqdm(total=len(vectors))
    for examined_point in vectors:
        center = np.array([0,0,0])
        line_vector = np.array([examined_point[4], examined_point[5], examined_point[6]])

        points_on_line = []
        for point in vectors:
            point_on_line = closest_point_on_line(
                center, line_vector, np.array([point[4], point[5], point[6]])
            )
            x, y, z = point_on_line[0], point_on_line[1], point_on_line[2]
            points_on_line.append((
                point[0], point[1], x, y, z 
            ))

        top = max(points_on_line, key=distance)
        tops_of_the_world.append((top[0], top[1]))
        pbar.update(1)

    unique_tops = []
    for top in tops_of_the_world:
        if top not in unique_tops:
            unique_tops.append(top)

    pbar.close()
    return unique_tops


def closest_point_on_line(a, b, p):
    ap = p-a
    ab = b-a
    result = a + np.dot(ap,ab)/np.dot(ab,ab) * ab
    return result


def distance(point):
    return np.sqrt(point[2]**2 + point[3]**2 + point[4]**2)


def save_file(input_file, tops_of_the_world):
    with rasterio.open(input_file) as src:
        profile = src.profile
        data = src.read()

    for x, y in tops_of_the_world:
        for i in range(100):
            if y+i < 6000:
                for j in range(100):
                    if x+j < 6000:
                        data[0][y+i][x+j] = 32000

    plot.show(data)

    with rasterio.open('output.tif', 'w', **profile) as dst:
        dst.write(data[0].astype(rasterio.int16), 1)


def main():
    input_file = 'srtm_40_02.tif'

    print("Reading lat long elevation data from the {} file...".format(input_file))
    lat_long_elev_data = get_geocoords_from_input(input_file)

    print("Converting lat long elevation data to xyz vectors...")
    vectors = geocoords_to_vectors(lat_long_elev_data)

    print("Marking tops of the world...")
    tops_of_the_world = mark_tops_of_the_world(vectors)

    print("Tops of the world (x, y):")
    print(tops_of_the_world)

    print("Saving output file...")
    save_file(input_file, tops_of_the_world)
    
   
if __name__ == "__main__":
    main()
        