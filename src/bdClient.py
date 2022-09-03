import os

from pymongo import MongoClient


class BDClient:

    def __init__(self):
        client = MongoClient(os.environ.get('MONGO_URL'))
        db = client.EB_Advocacia
        self.collection = db.data_clients

    def consult_client(self, client_id):
        consult = self.collection.find_one({"client_id": client_id})
        return consult
