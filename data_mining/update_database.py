import pymongo
import json
import os
from argparse import ArgumentParser
from typing import List, Tuple, Dict


def main():
    dto_file = parse_arguments()

    print('Reading data transfer objects from the {} file...'.format(dto_file))
    dto = read_dto_from_file(dto_file)

    print('Updating database...')
    update_database_with_dto(dto)

    print('Finished successfully!')


def parse_arguments() -> str:
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', default='local_tops.json', help='update database with tops from specific file')
    args = parser.parse_args()
    return args.file


def read_dto_from_file(output_file: str) -> List:
    with open(output_file, 'r') as file:
        dto = json.load(file)
        return dto


CONNECTION_FORMAT = os.environ['MONGO_URI_FORMAT']
USERNAME = os.environ['DATABASE_USERNAME']
PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_NAME = os.environ['DATABASE_NAME']
COLLECTION_NAME = os.environ['COLLECTION_NAME']
def update_database_with_dto(dto):
    with pymongo.MongoClient(CONNECTION_FORMAT.format(USERNAME, PASSWORD)) as client:
        collection = client[DATABASE_NAME][COLLECTION_NAME]
        collection.find_one({}, {'_id': 0, 'index': 0, 'tops': 0})


if __name__ == '__main__':
    main()
