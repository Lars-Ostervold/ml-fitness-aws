import json
from flask_cors import CORS
from flask import Flask, jsonify, request
import awsgi

BASE_ROUTE = "/workout"

app = Flask(__name__)
cors = CORS(app) #This only allows requests from the localhost. 

#This handler is for awsgi and the lambda functions
def handler(event, context):
    return awsgi.response(app, event, context)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route(BASE_ROUTE, methods=['GET']) #This expects JSON data containing the option values from the frontend.
def handle_api_request():
    return jsonify("hello world")
#     data = request.json  # Get the JSON data from the request body

#     # Extract the values from the data dictionary
#     option1_value = data.get('option1')
#     option2_value = data.get('option2')
#     option3_value = data.get('option3')
#     option4_value = data.get('option4')

#     # Call your Python script or function to generate the output
#     # Pass the option values as arguments and get the output
#     output = main(option1_value, option2_value, option3_value, option4_value)

#     # Return the output as a JSON response
#     return json.dumps(output)
# #---------------END FLASK CODE----------------------------------------


