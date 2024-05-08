from pymongo import MongoClient


class MongoDBSaver:
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]

    def save_cases(self, cases):
        for case in cases:
            self.collection.insert_one(case)
