from __future__ import annotations
from typing import Tuple, List
import nvector as nv
import numpy as np
import pymongo


def find_closest_top(latitude: float, longitude: float, collection: pymongo.collection.Collection, chunk_size: int) -> Tuple[float, float]:
    xyz = convert_latlong_to_xyz(latitude, longitude)
    indexes = calculate_indexes_for_xyz(xyz, chunk_size)
    # See https://stackoverflow.com/questions/5947137/how-can-i-use-a-list-comprehension-to-extend-a-list-in-python
    tops = [top for index in indexes for top in get_tops_for_index(index, collection)]
    closest_top = calculate_closest_top(xyz, tops)
    top_latitude, top_longitude = convert_xyz_to_latlong(closest_top)
    return top_latitude, top_longitude


def convert_latlong_to_xyz(latitude: float, longitude: float) -> np.ndarray:
    # See https://github.com/pbrod/nvector#example-4-geodetic-latitude-to-ecef-vector
    wgs84 = nv.FrameE(name='WGS84')
    pointB = wgs84.GeoPoint(latitude=latitude, longitude=longitude, z=0.0, degrees=True)
    xyz = pointB.to_ecef_vector().pvector.ravel()
    return xyz


# TODO:
def calculate_indexes_for_xyz(xyz: np.ndarray, chunk_size: int) -> List[np.ndarray]:
    x = xyz[0] - xyz[0] % chunk_size
    y = xyz[1] - xyz[1] % chunk_size
    z = xyz[2] - xyz[2] % chunk_size
    return [np.array([x, y, z])]


def get_tops_for_index(xyz: np.ndarray, collection: pymongo.collection.Collection) -> List[np.ndarray]:
    cursor = collection.find_one({'index': {'x': xyz[0], 'y': xyz[1], 'z': xyz[2]}}, {'_id': 0, 'index': 0})
    tops = [np.array([top['x'], top['y'], top['z']]) for top in cursor['tops']]
    return tops


def calculate_closest_top(xyz: np.ndarray, tops: List[np.ndarray]) -> np.ndarray:
    # The square root function is monotonic, so it can be discarded
    closest_top = min(tops, key=lambda item: ((xyz[0]-item[0])**2 + (xyz[1]-item[1])**2 + (xyz[2]-item[2])**2))
    return closest_top


def convert_xyz_to_latlong(xyz: np.ndarray) -> Tuple[float, float]:
    # See https://github.com/pbrod/nvector#example-3-ecef-vector-to-geodetic-latitude
    wgs84 = nv.FrameE(name='WGS84')
    position_B = 6371e3 * np.vstack((xyz[0], xyz[1], xyz[2]))
    latitude, longitude, _ = wgs84.ECEFvector(position_B).to_geo_point().latlon_deg
    return latitude, longitude
