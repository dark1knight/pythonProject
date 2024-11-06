# services/phone_call_service.py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .database_service import MongoDBContext
import pytz

class PhoneCallService:
    def __init__(self):
        self.db_context = MongoDBContext()
        self.phone_call_collection = self.db_context.phone_collection()

    def add_start_call(self, start_call_data):
        self.phone_call_collection.insert_one(start_call_data)

    def add_end_call(self, end_call_data):
        self.phone_call_collection.insert_one(end_call_data)
        start_call = self.phone_call_collection.find_one({
            "type": "start",
            "call_id": end_call_data["call_id"]
        })

        if start_call:
            start_timestamp = start_call["timestamp"]
            end_timestamp = end_call_data["timestamp"]

            if start_timestamp.tzinfo is None:
                start_timestamp = start_timestamp.replace(tzinfo=pytz.UTC)
            if end_timestamp.tzinfo is None:
                end_timestamp = end_timestamp.replace(tzinfo=pytz.UTC)

            call_duration = end_timestamp - start_timestamp
            call_price = self.calculate_price(start_timestamp, end_timestamp)

            pricing_record = {
                "call_id": end_call_data["call_id"],
                "type": "pricing",
                "call_duration": str(call_duration),
                "call_price": call_price,
                "source": start_call["source"],  
                "destination": start_call["destination"],
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp
            }

            self.phone_call_collection.insert_one(pricing_record)

    def calculate_price(self, start_timestamp, end_timestamp):
        # Define rates
        fixed_rate = 0.36
        per_minute_rate_standard = 0.09
        per_minute_rate_reduced = 0.00

        # Convert standard start and end times to timezone-aware in UTC
        standard_start = start_timestamp.replace(hour=6, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
        standard_end = start_timestamp.replace(hour=22, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)

        # Initialize price with fixed rate
        total_price = fixed_rate

        # Calculate total call duration in minutes (only full 60-second increments count)
        total_minutes = int((end_timestamp - start_timestamp).total_seconds() // 60)

        for minute in range(total_minutes):
            current_time = start_timestamp + timedelta(minutes=minute)

            # Ensure current_time is timezone-aware in UTC
            if current_time.tzinfo is None:
                current_time = current_time.replace(tzinfo=pytz.UTC)

            # Determine if the current minute is within standard or reduced rate times
            if standard_start <= current_time < standard_end:
                total_price += per_minute_rate_standard
            else:
                total_price += per_minute_rate_reduced

        return round(total_price, 2)

    def get_pricing_records_by_source_and_timeframe(self, source, year_month):
        # Parse year and month for timeframe
        start_date = datetime.strptime(year_month, "%Y-%m")
        end_date = start_date + relativedelta(months=1)

        # Query for pricing records with the given timeframe and source
        pricing_records = list(self.phone_call_collection.find({
        "type": "pricing",
        "source": source,
        "start_timestamp": {"$gte": start_date, "$lt": end_date}
    }, {"_id": 0}))

        return pricing_records
