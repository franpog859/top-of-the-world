from __future__ import annotations
from typing import Tuple, List
import nvector as nv
import numpy as np
import pymongo


def find_closest_top(latitude: float, longitude: float, collection: pymongo.collection.Collection, chunk_size: int) -> Tuple[float, float]:
    print('find_closest_top(latitude: float, longitude: float, collection: pymongo.collection.Collection, chunk_size: int) -> Tuple[float, float]:')
    xyz = convert_latlong_to_xyz(latitude, longitude)
    closest_top = calculate_closest_top_iteratively(xyz, collection, chunk_size)
    top_latitude, top_longitude = convert_xyz_to_latlong(closest_top)
    return top_latitude, top_longitude


def convert_latlong_to_xyz(latitude: float, longitude: float) -> np.ndarray:
    print('convert_latlong_to_xyz(latitude: float, longitude: float) -> np.ndarray:')
    # See https://github.com/pbrod/nvector#example-4-geodetic-latitude-to-ecef-vector
    xyz = nv.FrameE(name='WGS84') \
            .GeoPoint(latitude=latitude, longitude=longitude, z=0.0, degrees=True) \
            .to_ecef_vector() \
            .pvector.ravel()
    return xyz


NUMBER_OF_INDEX_LEVELS = 4 # math.ceil(safety_margin / chunk_size)
def calculate_closest_top_iteratively(xyz: np.ndarray, collection: pymongo.collection.Collection, chunk_size: int) -> np.ndarray:
    print('calculate_closest_top_iteratively(xyz: np.ndarray, collection: pymongo.collection.Collection, chunk_size: int) -> np.ndarray:')
    base_index = calculate_base_index(xyz, chunk_size)
    closest_top = np.empty((0, 3))
    for level in range(NUMBER_OF_INDEX_LEVELS):
        indexes = calculate_indexes_for_level(base_index, level, chunk_size)
        # See https://stackoverflow.com/questions/5947137/how-can-i-use-a-list-comprehension-to-extend-a-list-in-python
        tops = [top for index in indexes for top in get_tops_for_index(index, collection)]
        this_iteration_closest_top = calculate_closest_top(xyz, tops)
        closest_top = this_iteration_closest_top if level == 0 or calculate_distance(xyz, this_iteration_closest_top) > calculate_distance(xyz, closest_top) else closest_top
        if calculate_distance(xyz, closest_top) < calculate_shortest_distance_to_the_edge(xyz, level, chunk_size):
            return closest_top
    raise Exception("No tops found near the location")


def calculate_base_index(xyz: np.ndarray, chunk_size: int) -> np.ndarray:
    print('calculate_base_index(xyz: np.ndarray, chunk_size: int) -> np.ndarray:')
    return xyz - xyz % np.int(chunk_size)


def calculate_indexes_for_level(base_index: np.ndarray, level: int, chunk_size: int) -> np.ndarray:
    print('calculate_indexes_for_level(base_index: np.ndarray, level: int, chunk_size: int) -> np.ndarray:')
    indexes = np.empty((0, 3))
    for x in range(-level, level+1):
        for y in range(-level, level+1):
            for z in range(-level, level+1):
                # Add only chunks on the periphery
                if abs(x) == level or abs(y) == level or abs(z) == level:
                    indexes = np.append(indexes, [[
                        base_index[0] + x * np.int(chunk_size),
                        base_index[1] + y * np.int(chunk_size),
                        base_index[2] + z * np.int(chunk_size)]], axis=0)
                    # indexes = np.append(indexes, [[base_index + np.array([x, y, z] * np.int(chunk_size))]], axis=0)
    return indexes


def get_tops_for_index(xyz: np.ndarray, collection: pymongo.collection.Collection) -> List[np.ndarray]:
    print('get_tops_for_index(xyz: np.ndarray, collection: pymongo.collection.Collection) -> List[np.ndarray]:')
    cursor = collection.find_one({'index': {'x': xyz[0], 'y': xyz[1], 'z': xyz[2]}}, {'_id': 0, 'index': 0})
    return [np.array([top['x'], top['y'], top['z']]) for top in cursor['tops']]


def calculate_closest_top(xyz: np.ndarray, tops: List[np.ndarray]) -> np.ndarray:
    print('calculate_closest_top(xyz: np.ndarray, tops: List[np.ndarray]) -> np.ndarray:')
    return min(tops, key=lambda top: calculate_distance(xyz, top))


def calculate_distance(a: np.ndarray, b: np.ndarray) -> np.float:
    print('calculate_distance(a: np.ndarray, b: np.ndarray) -> np.float:')
    return np.linalg.norm(a - b)
   

def calculate_shortest_distance_to_the_edge(xyz: np.ndarray, level:int, chunk_size: int) -> np.float:
    print('calculate_shortest_distance_to_the_edge(xyz: np.ndarray, level:int, chunk_size: int) -> np.float:')
    return min([coordinate % np.int(chunk_size) for coordinate in xyz]) + level * np.int(chunk_size)


def convert_xyz_to_latlong(xyz: np.ndarray) -> Tuple[float, float]:
    print('convert_xyz_to_latlong(xyz: np.ndarray) -> Tuple[float, float]:')
    # See https://github.com/pbrod/nvector#example-3-ecef-vector-to-geodetic-latitude
    position_B = 6371e3 * np.vstack((xyz[0], xyz[1], xyz[2]))
    latitude, longitude, _ = nv.FrameE(name='WGS84') \
                               .ECEFvector(position_B) \
                               .to_geo_point().latlon_deg
    return float(latitude), float(longitude)
