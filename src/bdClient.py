import os

from pymongo import MongoClient


class BDClient:

    def __init__(self):
        client = MongoClient(os.environ.get('MONGO_URL'))
        db = client.EB_Advocacia
        self.collection = db.data_clients
        self.status_waiting_approval = False

    def consult_client(self, client_id):
        consult = self.collection.find_one({"client_id": client_id})
        return consult

    def insert_new_client(self, client_id, client_name):
        access_level = "Client"

        new_client = {"client_id": client_id, "client_name": client_name,
                      "access_level": access_level, "status": "Cadastrando"}
        insert_id = self.collection.insert_one(new_client).inserted_id
        return insert_id

    def consult_waiting_approval(self):
        waiting_approvals = self.collection.find({"status": self.status_waiting_approval})
        return waiting_approvals

    def update_client(self, id, key, value):
        issue = {key: value}
        myquery = {"_id": id}
        newvalues = {"$set": issue}
        self.collection.update_one(myquery, newvalues)

    def delete_document(self, client_id):
        self.collection.delete_one({"client_id": client_id})

    def consult_all_by_one_parameter(self, key, value):
        consult = self.collection.find({key: value})
        return consult
