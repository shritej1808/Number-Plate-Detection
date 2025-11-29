from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def insert_plate(plate_text):
    if plate_text:
        data = {"plate": plate_text}
        result = collection.insert_one(data)
        return result.inserted_id
    return None
