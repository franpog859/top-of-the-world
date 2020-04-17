from __future__ import annotations
from typing import Tuple, List
import pymongo


def find_closest_top(latitude: float, longitude: float, collection: pymongo.collection.Collection) -> Tuple[float, float]:
    xyz = convert_latlong_to_xyz(latitude, longitude)
    indexes = calculate_indexes_for_xyz(xyz)
    # See https://stackoverflow.com/questions/5947137/how-can-i-use-a-list-comprehension-to-extend-a-list-in-python
    tops = [top for index in indexes for top in get_tops_for_index(index, collection)]
    closest_top = calculate_closest_top(xyz, tops)
    top_latitude, top_longitude = convert_xyz_to_latlong(closest_top)
    return top_latitude, top_longitude


class XYZ:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


# TODO:
def convert_latlong_to_xyz(latitude: float, longitude: float) -> XYZ:
    return XYZ(1171, 2123, 1421)
def calculate_indexes_for_xyz(xyz: XYZ) -> List[XYZ]:
    return [XYZ(1000.0, 2000.0, 1000.0)]
def get_tops_for_index(xyz: XYZ, collection: pymongo.collection.Collection) -> List[XYZ]:
    cursor = collection.find_one({'index': {'x': xyz.x, 'y': xyz.y, 'z': xyz.z}}, {'_id': 0, 'index': 0})
    tops = [XYZ(top['x'], top['y'], top['z']) for top in cursor['tops']]
    return tops
def calculate_closest_top(xyz: XYZ, tops: List[XYZ]) -> XYZ:
    closest_top = min(tops, key=lambda item:
        # The square root function is monotonic, so it can be discarded
        ((xyz.x-item.x)**2 + (xyz.y-item.y)**2 + (xyz.z-item.z)**2))
    return closest_top
def convert_xyz_to_latlong(xyz: XYZ) -> Tuple[float, float]:
    return 123.42, -32.123

