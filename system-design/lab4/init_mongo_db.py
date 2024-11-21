from pymongo import MongoClient

# Настройка Mongo
MONGODB_URI = "mongodb://root:rootpasswd@mongo:27017/"   

# Подключение к MongoDB
client = MongoClient(MONGODB_URI)

# Выбор базы данных
db = client['mongo_profi_db']

# Выбор коллекции
collection = db['users']

# MONGO_URI = "mongodb://root:pass@mongo:27017/"
# mongo_client = MongoClient(MONGO_URI)
# mongo_db = mongo_client["mongo_profi_db"]
# mongo_users_collection = mongo_db["users"]

# print("``````````````", mongo_users_collection)


document = {
    'name': 'Jirome K Jirome',
    'age': 10,
    'email': 'kj@example.com'
}

# Insert the document into the collection 
result = collection.insert_one(document)
# Check if the insertion was successful
if result.acknowledged:
    print('```````Document inserted successfully.')
    print('```````Inserted document ID:', result.inserted_id) 
else:
    print('```````Failed to insert document.')