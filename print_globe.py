from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import nvector as nv
from tqdm import tqdm


def main():
    input_file = 'data/srtm_40_02.tif'  # TODO: Do not hardcode it. Use a script parameter
    step = 180  # TODO: Add counting step function to be relative to the image size

    print("Reading lat long elevation data from the {} file...".format(input_file))
    latlongelev_list = get_latlongelev_list_from_tif_image(input_file, step)

    print("Converting lat long elevation data to xyz vectors...")
    points = latlongelev_list_to_xyz_list(latlongelev_list)
    plotGlobe(points)

    print("Marking tops of the world...")
    tops_of_the_world = filter_only_tops(points)
    plotGlobe(tops_of_the_world)

    # print("Saving output file...")
    # save_file(input_file, tops_of_the_world, step)

    # print("Tops of the world saved successfully!")


def plotGlobe(xyz_list: list(XYZ)):
    x = []
    y = []
    z = []
    for point in xyz_list:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    plt.show()


class LatLongElev:
    def __init__(self, latitude: float, longitude: float, elevation: float=0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation


class XYZ:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def project_onto_line(self, _a: XYZ, _b: XYZ) -> XYZ:
        # See https://gamedev.stackexchange.com/questions/72528/how-can-i-project-a-3d-point-onto-a-3d-line
        p = self.to_np_array()
        a = _a.to_np_array()
        b = _b.to_np_array()
        ap = p-a
        ab = b-a
        result = a + np.dot(ap, ab)/np.dot(ab, ab) * ab
        return XYZ(result[0], result[1], result[2])

    def to_np_array(self) -> np.array:
        return np.array([self.x, self.y, self.z])


DEEPEST_DEPRESSION_ON_EARTH = -418.0
def get_latlongelev_list_from_tif_image(image_file: str, step: int=1) -> list(LatLongElev):
    latlongelev_list = []
    with rasterio.open(image_file) as image:
        elevation_values = image.read(1)
        for y in range(0, image.height, step):
            for x in range(0, image.width, step):
                longitude, latitude = image.xy(y, x)
                elevation = elevation_values[y, x]
                # Clean under the sea elevations
                elevation = elevation if elevation > DEEPEST_DEPRESSION_ON_EARTH else DEEPEST_DEPRESSION_ON_EARTH
                latlongelev_list.append(LatLongElev(latitude, longitude, elevation))
    return latlongelev_list


def latlongelev_list_to_xyz_list(latlongelev_list: list(LatLongElev)) -> list(XYZ):
    # See https://github.com/pbrod/nvector#example-4-geodetic-latitude-to-ecef-vector
    wgs84 = nv.FrameE(name='WGS84') 
    xyz_list = []
    for latlongelev in latlongelev_list:
        depth = latlongelev.elevation * (-1)
        pointB = wgs84.GeoPoint(latitude=latlongelev.latitude, longitude=latlongelev.longitude, z=depth, degrees=True)
        p_EB_E = pointB.to_ecef_vector()
        x, y, z = p_EB_E.pvector.ravel()[0], p_EB_E.pvector.ravel()[1], p_EB_E.pvector.ravel()[2]
        xyz_list.append(XYZ(x, y, z))
    return xyz_list


def filter_only_tops(xyz_list: list(XYZ)) -> list(XYZ):
    progress_bar = tqdm(total=len(xyz_list))
    top_list = []
    for xyz in xyz_list:
        top = _get_top_for_direction(xyz, xyz_list)
        # Store only unique tops
        if top not in top_list: 
            top_list.append(top)
        progress_bar.update(1)
    progress_bar.close()
    return top_list


CENTER_OF_THE_EARTH = XYZ(0, 0, 0)
def _get_top_for_direction(direction: XYZ, xyz_list: list(XYZ)) -> XYZ:
    xyz_projection_list = []
    for xyz in xyz_list:
        xyz_projection = xyz.project_onto_line(CENTER_OF_THE_EARTH, direction)
        if _are_on_the_same_side_relative_to_center(xyz_projection, direction):
            xyz_projection_list.append(xyz_projection)

    top = max(xyz_projection_list, key=_distance)
    return top


def _are_on_the_same_side_relative_to_center(a: XYZ, b: XYZ) -> bool:
    signs = np.sign([a.x, b.x, a.y, b.y, a.z, b.z])
    for axis in range(3):
        if signs[0+axis] == signs[1+axis]:
            return True
    return False


def _distance(xyz: XYZ) -> float:
    # The square root function is monotonic, so it can be discarded
    return xyz.x**2 + xyz.y**2 + xyz.z**2


if __name__ == "__main__":
    main()
