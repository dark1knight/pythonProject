# controllers/phone_call_controller.py

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from services.phone_call_service import PhoneCallService
from models.call_record import CallStartRecord, CallEndRecord
from models.pricing_record import PricingRecord
from pydantic import ValidationError

# Initialize the phone call service
phone_call_service = PhoneCallService()

# Define the namespace for the phone calls
api = Namespace("phone_calls", description="Operations related to phone calls")

# Swagger models
start_call_model = api.model("StartCall", {
    "call_id": fields.Integer(required=True, description="Unique call identifier"),
    "type": fields.String(required=True, description="Type of call (start)", enum=["start"]),
    "timestamp": fields.DateTime(required=True, description="Call start timestamp in ISO format"),
    "source": fields.String(required=True, description="Caller phone number"),
    "destination": fields.String(required=True, description="Recipient phone number")
})

end_call_model = api.model("EndCall", {
    "call_id": fields.Integer(required=True, description="Unique call identifier"),
    "type": fields.String(required=True, description="Type of call (end)", enum=["end"]),
    "timestamp": fields.DateTime(required=True, description="Call end timestamp in ISO format")
})

pricing_query_model = api.model("PricingQuery", {
    "source": fields.String(required=True, description="Caller phone number"),
    "timeframe": fields.String(required=True, description="Timeframe in YYYY-MM format")
})

pricing_query_params = api.parser()
pricing_query_params.add_argument('source', type=str, required=True, location='args', help="Caller phone number")
pricing_query_params.add_argument('timeframe', type=str, required=True, location='args', help="Timeframe in YYYY-MM format")

pricing_record_model = api.model("PricingRecord", {
    "call_id": fields.Integer(description="Unique call identifier"),
    "type": fields.String(description="Record type, always 'pricing'"),
    "call_duration": fields.String(description="Duration of the call in HH:MM:SS format"),
    "call_price": fields.Float(description="Calculated price of the call"),
    "source": fields.String(description="Caller phone number"),
    "destination": fields.String(description="Recipient phone number"),
    "start_timestamp": fields.DateTime(description="Call start timestamp"),
    "end_timestamp": fields.DateTime(description="Call end timestamp")
})

# Define the endpoints
@api.route('/start')
class StartCallResource(Resource):
    @api.expect(start_call_model)
    def post(self):
        """Add a new start call record"""
        try:
            # Parse and validate the request data with Pydantic
            phone_call_data = CallStartRecord.parse_obj(request.json)
            phone_call_service.add_start_call(phone_call_data.dict())
            return {"message": "Start call record added successfully"}, 201
        except ValidationError as e:
            return {"error": e.errors()}, 400


@api.route('/end')
class EndCallResource(Resource):
    @api.expect(end_call_model)
    def post(self):
        """Add a new end call record and calculate pricing"""
        try:
            # Parse and validate the request data with Pydantic
            phone_call_data = CallEndRecord.parse_obj(request.json)
            phone_call_service.add_end_call(phone_call_data.dict())
            return {"message": "End call record added successfully"}, 201
        except ValidationError as e:
            return {"error": e.errors()}, 400


@api.route('/search')
class PricingQueryResource(Resource):
    @api.expect(pricing_query_params, validate=False)  # Allow optional validation
    @api.marshal_list_with(pricing_record_model)
    def get(self):
        """Retrieve call pricing records by source and optional timeframe"""
        source = request.args.get('source')
        year_month = request.args.get('timeframe')  # Optional parameter
        
        # Validate that 'source' is present
        if not source:
            return {"error": "'source' parameter is required"}, 400
        
        try:
            # Call the service method with 'year_month' (can be None)
            result = phone_call_service.get_pricing_records_by_source_and_timeframe(source, year_month)
            return result
        except ValueError as e:
            return {"error": str(e)}, 400
