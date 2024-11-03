# main.py
from flask import Flask, request, jsonify
from models.call_record import CallStartRecord, CallEndRecord
from services.call_service import CallService

app = Flask(__name__)
call_service = CallService()

@app.route('/api/start_call', methods=['POST'])
def start_call():
    data = request.json
    record = CallStartRecord(**data)
    call_service.add_record(record)
    return jsonify(record.dict()), 201

@app.route('/api/end_call', methods=['POST'])
def end_call():
    data = request.json
    record = CallEndRecord(**data)
    call_service.add_record(record)
    return jsonify(record.dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
