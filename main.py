# main.py

from flask import Flask
from flask_restx import Api
from controllers.phone_call_controller import api as phone_calls_ns

# Initialize the Flask application
app = Flask(__name__)

# Initialize the Flask-RESTx API
api = Api(app, version="1.0", title="Call Records API", description="A simple API for call records")

# Register the phone_calls namespace from the controller
api.add_namespace(phone_calls_ns, path="/api/phone_calls")

if __name__ == "__main__":
    app.run(debug=True)

