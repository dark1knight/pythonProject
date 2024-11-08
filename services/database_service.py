
import os
from pymongo import MongoClient

class MongoDBContext:
    def __init__(self):
        # Read the MongoDB URI from the environment variable
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
        
        # Initialize MongoDB client with the URI from the environment variable
        #self.client = MongoClient(mongo_uri)
        self.client = MongoClient(mongo_uri)
        self._database = self.client["Call"]  

    def get_collection(self, collection_name):
        return self._database[collection_name]

    def phone_collection(self):
        return self.get_collection("PhoneCall")
