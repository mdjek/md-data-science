import json
from pymongo import MongoClient

# Настройка Mongo
MONGODB_URI = "mongodb://root:rootpasswd@mongo:27017/"   
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=1000)
db = client['mongo_profi_db']
collection = db['users']

def load_mongo_collection_mock(data: list):
    for entity in data:
        result = collection.insert_one(entity)

        if result.acknowledged:
            print('Document inserted successfully (MongoDB).')    
        else:
            print('Failed to insert document (MongoDB).')

def load_mongo_mock_data():
    mock_map = ("users",)

    for key in mock_map:
        f_opened = open(f"./mocks/{key}.json")
        data = json.load(f_opened)

        load_mongo_collection_mock(data)
        f_opened.close()