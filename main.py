# main.py
from flask import Flask, jsonify
from services.phone_call_service import PhoneCallService

app = Flask(__name__)
phone_call_service = PhoneCallService()

# Basic route to display a welcome message
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Call Records API!"}), 200

@app.route('/api/phone_calls', methods=['POST'])
def add_phone_call():
    phone_call_data = request.json
    phone_call_service.add_phone_call(phone_call_data)
    return jsonify({"message": "Phone call record added successfully"}), 201

@app.route('/api/phone_calls', methods=['GET'])
def get_phone_calls():
    phone_calls = phone_call_service.get_all_phone_calls()
    return jsonify(phone_calls), 200

if __name__ == '__main__':
    app.run(debug=True)

