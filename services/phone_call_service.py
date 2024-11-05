from datetime import datetime
from dateutil.relativedelta import relativedelta
from bson import ObjectId
from .database_service import MongoDBContext

class PhoneCallService:
    def __init__(self):
        self.db_context = MongoDBContext()
        self.phone_call_collection = self.db_context.phone_collection()

    def add_start_call(self, start_call_data):
        """Insert a new start call record into the 'PhoneCall' collection."""
        self.phone_call_collection.insert_one(start_call_data)

    def add_end_call(self, end_call_data):
        """Insert a new end call record into the 'PhoneCall' collection."""
        self.phone_call_collection.insert_one(end_call_data)

    def get_calls_by_source_and_timeframe(self, source, year_month):
        # Parse year and month for timeframe
        start_date = datetime.strptime(year_month, "%Y-%m")
        end_date = start_date + relativedelta(months=1)

        start_calls = list(self.phone_call_collection.find({
            "type": "start",
            "source": source,
            "timestamp": {"$gte": start_date, "$lt": end_date}
        }))

        paired_calls = []
        for start_call in start_calls:
            end_call = self.phone_call_collection.find_one({
                "type": "end",
                "call_id": start_call["call_id"]
            })

            if end_call:
                start_timestamp = start_call["timestamp"]
                end_timestamp = end_call["timestamp"]
                call_duration = end_timestamp - start_timestamp

                paired_calls.append({
                    "destination": start_call["destination"],
                    "start_timestamp": start_timestamp,
                    "end_timestamp": end_timestamp,
                    "call_duration": str(call_duration),  
                    "call_price": None  
                })

        return paired_calls