import json
from pymongo import ASCENDING, MongoClient

MOCK_TABLE_LIST = ("users",)

# Настройка Mongo
MONGODB_URI = "mongodb://root:rootpasswd@mongo:27017/"   
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=1000)
db = client['mongo_profi_db']
collection = db['users']
# Создание индекса на поле username
# collection.create_index([("username", ASCENDING)], unique=True)

def load_mongo_collection_mock(data: list):
    existCollection = list(collection.find())
    
    # если есть записи – не добавляем
    if len(existCollection):
        return

    for entity in data:
        result = collection.insert_one(entity)

        if result.acknowledged:
            print('Document inserted successfully (MongoDB).')    
        else:
            print('Failed to insert document (MongoDB).')

def load_mongo_mock_data():
    for key in MOCK_TABLE_LIST:
        f_opened = open(f"./mocks/{key}.json")
        data = json.load(f_opened)

        load_mongo_collection_mock(data)
        f_opened.close()