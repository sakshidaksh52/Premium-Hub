import os
import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection setup
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['telegram_bot']
users_collection = db['users']
file_storage_collection = db['file_storage']

# Test MongoDB connection
def ping_db():
    try:
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return False
