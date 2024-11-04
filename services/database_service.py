
from pymongo import MongoClient

class MongoDBContext:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://nakamutaADM:Swordman11@mycluster.hk6ns.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster")
        self._database = self.client["Call"]  

    def get_collection(self, collection_name):
        return self._database[collection_name]

    def phone_collection(self):
        return self.get_collection("PhoneCall")
