from __future__ import annotations
from argparse import ArgumentParser
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import nvector as nv
from typing import List, Tuple


def main():
    input_file, step, output_file, should_omit_saving, should_mark_on_margin, should_plot = parse_arguments()

    print("Reading lat long elevation data from the {} file...".format(input_file))
    latlongelev_list = get_latlongelev_list_from_tif_image(input_file, step)

    print("Converting lat long elevation data to xyz points...")
    points = latlongelev_list_to_xyz_list(latlongelev_list)
    if should_plot:
        print("Plotting map...")
        plotGlobe(points)

    print("Marking tops of the world...")
    tops = filter_only_tops(points)
    # TODO:
    # if not should_mark_on_margin:
    #     print("Filtering tops on the map's margin...")
    #     tops = filter_out_of_margin(tops)

    if should_plot:
        print("Plotting tops of the world...")
        plotGlobe(tops)

    # TODO:
    # if not should_omit_saving:
    #     print("Saving tops to the {} file...".format(output_file))
    #     save_results_to_local_file(tops, output_file)

    print("Finished successfully!")


def parse_arguments() -> Tuple[str, int, str, bool, bool, bool]:
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="use a map from *.tif file")
    parser.add_argument("-s", "--step", type=int, default=1, help="don't use all pixels - go with a step")
    parser.add_argument("-o", "--output", default="local_tops.json", help="save result to specific file")
    parser.add_argument("-d", "--dummy", action="store_true", help="do not save results to the local file")
    parser.add_argument("-m", "--margin", action="store_true", help="mark tops also on the map's margin")
    parser.add_argument("-p", "--plot", action="store_true", help="plot the map and the map with the tops")
    args = parser.parse_args()
    return args.file, args.step, args.output, args.dummy, args.margin, args.plot


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

    def __eq__(self, xyz: XYZ) -> bool:
        return self.x == xyz.x and self.y == xyz.y and self.z == xyz.z

    def __str__(self) -> str:
        return "x={}, y={}, z={}".format(self.x, self.y, self.z)

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


def plotGlobe(xyz_list: List(XYZ)):
    x = [xyz.x for xyz in xyz_list]
    y = [xyz.y for xyz in xyz_list]
    z = [xyz.z for xyz in xyz_list]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    plt.show()



DEEPEST_DEPRESSION_ON_EARTH = -418.0
def get_latlongelev_list_from_tif_image(image_file: str, step: int=1) -> List(LatLongElev):
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


def latlongelev_list_to_xyz_list(latlongelev_list: List(LatLongElev)) -> List(XYZ):
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


def filter_only_tops(xyz_list: List(XYZ)) -> List(XYZ):
    progress_bar = tqdm(total=len(xyz_list))
    top_list = []
    for xyz in xyz_list:
        top = get_top_for_direction(xyz, xyz_list)
        # Store only unique tops
        if top not in top_list: 
            top_list.append(top)
        progress_bar.update(1)
    progress_bar.close()
    return top_list


CENTER_OF_THE_EARTH = XYZ(0, 0, 0)
def get_top_for_direction(direction: XYZ, xyz_list: List(XYZ)) -> XYZ:
    xyz_projection_list = []
    for xyz in xyz_list:
        xyz_projection = xyz.project_onto_line(CENTER_OF_THE_EARTH, direction)
        if are_on_the_same_side_relative_to_center(xyz_projection, direction):
            xyz_projection_list.append((xyz, xyz_projection))

    top = max(xyz_projection_list, key=lambda item: _distance(item[1]))[0]
    return top


def are_on_the_same_side_relative_to_center(a: XYZ, b: XYZ) -> bool:
    signs = np.sign([a.x, b.x, a.y, b.y, a.z, b.z])
    for axis in range(0, 6, 2):
        if signs[0+axis] != signs[1+axis]:
            return False
    return True


def _distance(xyz: XYZ) -> float:
    # The square root function is monotonic, so it can be discarded
    return xyz.x**2 + xyz.y**2 + xyz.z**2


if __name__ == "__main__":
    main()
