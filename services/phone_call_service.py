# services/phone_call_service.py
from .database_service import MongoDBContext

class PhoneCallService:
    def __init__(self):
        self.db_context = MongoDBContext()
        self.phone_call_collection = self.db_context.phone_collection()

    def add_start_call(self, start_call_data):
        """Insert a new start call record into the 'PhoneCall' collection."""
        # Add any additional logic specific to start calls if needed
        self.phone_call_collection.insert_one(start_call_data)

    def add_end_call(self, end_call_data):
        """Insert a new end call record into the 'PhoneCall' collection."""
        # Add any additional logic specific to end calls if needed
        self.phone_call_collection.insert_one(end_call_data)

    def get_all_phone_calls(self):
        """Retrieve all phone call records from the 'PhoneCall' collection."""
        return list(self.phone_call_collection.find())
