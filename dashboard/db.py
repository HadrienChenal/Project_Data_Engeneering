from pymongo import MongoClient

def get_games():
    client = MongoClient("mongodb://localhost:27017")
    db = client["steam_db"]
    return list(db["games"].find({}, {"_id": 0}))
