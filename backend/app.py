from __future__ import annotations
import numpy as np
import logging
import pymongo
import os
from typing import Tuple, List
import nvector as nv
from flask import Flask, jsonify, request
app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

app.logger.info('reading database environment variables')
connection_format = os.environ['MONGO_URI_FORMAT'] 
username = os.environ['DATABASE_USERNAME'] 
password = os.environ['DATABASE_PASSWORD'] 
database_name = os.environ['DATABASE_NAME'] 
collection_name = os.environ['COLLECTION_NAME'] 

AUTH_TOKEN='totalsecuretoken123'
AUTH_TOKEN_HEADER_KEY='token'


@app.route('/healthz', methods=['GET'])
def healthz():
    app.logger.info('GET /healthz')
    if request.headers.get(AUTH_TOKEN_HEADER_KEY) != AUTH_TOKEN:
        app.logger.warning('failed to authenticate')
        return jsonify(error='failed to authenticate'), 403
    try:
        with pymongo.MongoClient(connection_format.format(username, password)) as client:
            collection = client[database_name][collection_name]
            collection.find_one({}, {'_id': 0, 'index': 0, 'tops': 0})   
            app.logger.info('database connection succeeded')
    except Exception as e:
        app.logger.error('failed to connect to the database: {}'.format(str(e)))
        return jsonify(error='failed to connect to the database'), 500
    app.logger.info('server is healthy')
    return jsonify(status='healthy'), 200


@app.route('/closestTop/<float(signed=True):latitude>/<float(signed=True):longitude>', methods=['GET'])
def closest_top(latitude, longitude):
    app.logger.info('GET /closestTop')
    if request.headers.get(AUTH_TOKEN_HEADER_KEY) != AUTH_TOKEN:
        app.logger.warning('failed to authenticate')
        return jsonify(error='failed to authenticate'), 403

    app.logger.info('finding the closest top for lat={}, long={}'.format(latitude, longitude))
    try:
        with pymongo.MongoClient(connection_format.format(username, password)) as client:
            collection = client[database_name][collection_name]
            top_latitude, top_longitude = find_closest_top(latitude, longitude, collection)
    except Exception as e:
        app.logger.error('failed to find the closest top: {}'.format(str(e)))
        return jsonify(error='failed to find the closest top'), 500

    app.logger.info('closest top found successfully')
    return jsonify(latitude=top_latitude, longitude=top_longitude), 200


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


# TODO:
def convert_latlong_to_xyz(latitude: float, longitude: float) -> XYZ:
    return XYZ(1171, 2123, 1421)
def calculate_indexes_for_xyz(xyz: XYZ) -> List(XYZ):
    return [XYZ(1000.0, 2000.0, 1000.0)]
def get_tops_for_index(xyz: XYZ, collection: pymongo.collection.Collection) -> List(XYZ):
    cursor = collection.find_one({'index': {'x': xyz.x, 'y': xyz.y, 'z': xyz.z}}, {'_id': 0, 'index': 0})   
    tops = [XYZ(top['x'], top['y'], top['z']) for top in cursor['tops']]
    return tops
def calculate_closest_top(xyz: XYZ, tops: List(XYZ)) -> XYZ:
    closest_top = min(tops, key=lambda item:
        # The square root function is monotonic, so it can be discarded
        ((xyz.x-item.x)**2 + (xyz.y-item.y)**2 + (xyz.z-item.z)**2))
    return closest_top
def convert_xyz_to_latlong(xyz: XYZ) -> Tuple[float, float]:
    return 123.42, -32.123


if __name__ == '__main__':
    app.run()
