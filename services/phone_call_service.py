
from .database_service import MongoDBContext

class PhoneCallService:
    def __init__(self):
        self.db_context = MongoDBContext()
        self.phone_call_collection = self.db_context.phone_collection()

    def add_phone_call(self, phone_call_data):
        """Insert a new phone call record into the 'PhoneCall' collection."""
        self.phone_call_collection.insert_one(phone_call_data)

    def get_all_phone_calls(self):
        """Retrieve all phone call records from the 'PhoneCall' collection."""
        return list(self.phone_call_collection.find())
