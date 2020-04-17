import logging
import pymongo
import os
from lib.closest_top import find_closest_top
from flask import Flask, jsonify, request


app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

app.logger.info('reading environment variables')
CONNECTION_FORMAT = os.environ['MONGO_URI_FORMAT']
USERNAME = os.environ['DATABASE_USERNAME']
PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_NAME = os.environ['DATABASE_NAME']
COLLECTION_NAME = os.environ['COLLECTION_NAME']
AUTH_TOKEN = os.environ['AUTH_TOKEN']

AUTH_TOKEN_HEADER_KEY = 'token'


@app.route('/healthz', methods=['GET'])
def healthz():
    app.logger.info('GET /healthz')
    if request.headers.get(AUTH_TOKEN_HEADER_KEY) != AUTH_TOKEN:
        app.logger.warning('failed to authenticate')
        return jsonify(error='failed to authenticate'), 403
    try:
        with pymongo.MongoClient(CONNECTION_FORMAT.format(USERNAME, PASSWORD)) as client:
            collection = client[DATABASE_NAME][COLLECTION_NAME]
            collection.find_one({}, {'_id': 0, 'index': 0, 'tops': 0})
            app.logger.info('database connection succeeded')
    except Exception as e:
        app.logger.error('failed to connect to the database: {}'.format(str(e)))
        return jsonify(error='failed to connect to the database'), 500
    app.logger.info('server is healthy')
    return jsonify(status='healthy'), 200


@app.route('/closestTop/<float(signed=True):latitude>/<float(signed=True):longitude>', methods=['GET'])
def closest_top(latitude: float, longitude: float):
    app.logger.info('GET /closestTop')
    if request.headers.get(AUTH_TOKEN_HEADER_KEY) != AUTH_TOKEN:
        app.logger.warning('failed to authenticate')
        return jsonify(error='failed to authenticate'), 403

    app.logger.info('finding the closest top for lat={}, long={}'.format(latitude, longitude))
    try:
        with pymongo.MongoClient(CONNECTION_FORMAT.format(USERNAME, PASSWORD)) as client:
            collection = client[DATABASE_NAME][COLLECTION_NAME]
            top_latitude, top_longitude = find_closest_top(latitude, longitude, collection)
    except Exception as e:
        app.logger.error('failed to find the closest top: {}'.format(str(e)))
        return jsonify(error='failed to find the closest top'), 500

    app.logger.info('closest top found successfully')
    return jsonify(latitude=top_latitude, longitude=top_longitude), 200


if __name__ == '__main__':
    app.run()
