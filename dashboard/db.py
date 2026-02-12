import os
from pymongo import MongoClient

def get_games():
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["steam_db"]
    return list(db["games"].find({}, {"_id": 0}))
