import pymongo
from itemadapter import ItemAdapter
from datetime import datetime
import os

class SteamScraperPipeline:

    def open_spider(self, spider):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client["steam_db"]
        self.collection = self.db["games"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        data["scraped_at"] = datetime.utcnow()

        self.collection.update_one(
            {"steam_id": data["steam_id"]},
            {"$set": data},
            upsert=True
        )

        return item
