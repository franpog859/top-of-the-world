import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.plot as plot
import nvector as nv
from tqdm import tqdm


def main():
    input_file = 'srtm_40_02.tif'
    step = 100 # TODO: Add counting step function to be relative to the image size

    print("Reading lat long elevation data from the {} file...".format(input_file))
    lat_long_elev_data = get_geocoords_from_input(input_file, step)

    print("Converting lat long elevation data to xyz vectors...")
    vectors = geocoords_to_vectors(lat_long_elev_data)

    print("Marking tops of the world...")
    tops_of_the_world = get_tops_of_the_world(vectors)

    print("Saving output file...")
    save_file(input_file, tops_of_the_world, step)

    print("Tops of the world saved successfully!")


def get_geocoords_from_input(input_file, step):
    with rasterio.open(input_file) as src:
        plot.show(src)
        elevation_values = src.read(1)
        lat_long_elev_data = []
        # Range is limited due to long execution time. for y in range(src.height):
        for y in range(0, src.height, step): 
            # Range is limited due to long execution time. for x in range(src.width):
            for x in range(0, src.width, step): 
                longitude, latitude = src.xy(y,x)
                elevation = elevation_values[y,x]
                elevation = elevation if elevation > -100 else 0 # Cleaning sea data
                lat_long_elev_data.append((
                    x, y, latitude, longitude, elevation
                ))
    return lat_long_elev_data


def geocoords_to_vectors(lat_long_elev_data):
    wgs84 = nv.FrameE(name='WGS84')
    vectors = []
    for width, height, latitude, longitude, elevation in lat_long_elev_data:
        depth = elevation * (-1)
        pointB = wgs84.GeoPoint(
            latitude=latitude, longitude=longitude, z=depth, degrees=True
        )
        p_EB_E = pointB.to_ecef_vector()
        x, y, z = p_EB_E.pvector.ravel()[0], p_EB_E.pvector.ravel()[1], p_EB_E.pvector.ravel()[2]
        vectors.append((
            width, height, x, y, z
        ))
    return vectors


def get_tops_of_the_world(vectors):
    pbar = tqdm(total=len(vectors))

    tops_of_the_world = []
    for point in vectors:
        center = np.array([0,0,0])
        line_vector = np.array([point[2], point[3], point[4]])

        top = get_top_for_vector(center, line_vector, vectors)
        tops_of_the_world.append((top[0], top[1]))

        pbar.update(1)

    unique_tops = []
    for top in tops_of_the_world:
        if top not in unique_tops:
            unique_tops.append(top)

    pbar.close()
    return unique_tops


def get_top_for_vector(a, b, vectors):
    points_on_line = []
    for point in vectors:
        point_on_line = closest_point_on_line(
            a, b, np.array([point[2], point[3], point[4]])
        )
        x, y, z = point_on_line[0], point_on_line[1], point_on_line[2]
        points_on_line.append((
            point[0], point[1], x, y, z 
        ))

    top = max(points_on_line, key=distance)
    return top


def closest_point_on_line(a, b, p): # TODO: Check how it really works
    ap = p-a
    ab = b-a
    result = a + np.dot(ap,ab)/np.dot(ab,ab) * ab
    return result


def distance(point):
    return np.sqrt(point[2]**2 + point[3]**2 + point[4]**2)


def save_file(input_file, tops_of_the_world, step):
    with rasterio.open(input_file) as src:
        profile = src.profile
        data = src.read()
        width = src.width
        height = src.height

    for x, y in tops_of_the_world:
        for i in range(step):
            if y+i < height:
                for j in range(step):
                    if x+j < width:
                            data[0][y+i][x+j] = 32000

    with rasterio.open('output.tif', 'w', **profile) as dst:
        dst.write(data[0].astype(rasterio.int16), 1) 
        """
        TODO: Find the bug! It seems to mark the points that are NOT 
        actually the tops of the world. Like depressions and seas.
        Higher points like mountains are not marked!
        """

    plot.show(data)


if __name__ == "__main__":
    main()
        