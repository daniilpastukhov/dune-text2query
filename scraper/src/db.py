import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class MongoDatabase:
    def __init__(self) -> None:
        self.client = MongoClient(os.environ['MONGO_URI'])
        self.collection = self.client['db']['queries']

    def insert_one(self, doc):
        self.client.insert_one(doc)

    def get_total_queries(self):
        return self.client.count_documents({})

    def get_n_queries(self, n=-1):
        if n == -1:
            return self.collection.find({})
        return self.collection.find({}).limit(n)