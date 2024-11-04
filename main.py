
from flask import Flask, request, jsonify
from pydantic import ValidationError
from models.call_record import CallStartRecord, CallEndRecord
from services.phone_call_service import PhoneCallService

app = Flask(__name__)
phone_call_service = PhoneCallService()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Call Records API!"}), 200


@app.route('/api/phone_calls/start', methods=['POST'])
def add_start_call():
    phone_call_data = request.json
    try:
        # Validate with CallStartRecord model
        valid_data = CallStartRecord(**phone_call_data)
        phone_call_service.add_start_call(valid_data.dict())  # Use add_start_call method
        return jsonify({"message": "Start call record added successfully"}), 201
    except ValidationError as e:
        # Return error if validation fails
        return jsonify({"error": e.errors()}), 422


@app.route('/api/phone_calls/end', methods=['POST'])
def add_end_call():
    phone_call_data = request.json
    try:
        # Validate with CallEndRecord model
        valid_data = CallEndRecord(**phone_call_data)
        phone_call_service.add_end_call(valid_data.dict())  # Use add_end_call method
        return jsonify({"message": "End call record added successfully"}), 201

    except ValidationError as e:
        # Return error if validation fails
        return jsonify({"error": e.errors()}), 422

if __name__ == '__main__':
    app.run(debug=True)

