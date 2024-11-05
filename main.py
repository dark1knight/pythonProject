
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
        valid_data = CallStartRecord(**phone_call_data)
        phone_call_service.add_start_call(valid_data.dict())  # Use add_start_call method
        return jsonify({"message": "Start call record added successfully"}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422


@app.route('/api/phone_calls/end', methods=['POST'])
def add_end_call():
    phone_call_data = request.json
    try:
        valid_data = CallEndRecord(**phone_call_data)
        phone_call_service.add_end_call(valid_data.dict())  
        return jsonify({"message": "End call record added successfully"}), 201

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422
    

@app.route('/api/phone_calls/search', methods=['GET'])
def get_calls_by_source_and_timeframe():
    source = request.args.get('source')
    timeframe = request.args.get('timeframe')

    if not source or not timeframe:
        return jsonify({"error": "Both 'source' and 'timeframe' parameters are required"}), 400

    try:
        result = phone_call_service.get_calls_by_source_and_timeframe(source, timeframe)
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

