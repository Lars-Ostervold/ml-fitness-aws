#Send w/ 'amplify push -y'
import json
from flask_cors import CORS
from flask import Flask, jsonify, request
import urllib3
from generateWorkoutBackend import main


BASE_ROUTE = "/workout"
http = urllib3.PoolManager()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route(BASE_ROUTE, methods=['POST']) #This expects JSON data containing the option values from the frontend.
def handle_api_request():
    payload = request.get_json()
    
    data = payload.get('payload')  # Get the JSON data from the request body

    # Extract the values from the data dictionary
    workout_days_per_week = int(data.get('option1'))
    time_per_workout = int(data.get('option2'))
    fitness_goal = int(data.get('option3'))
    user_experience = int(data.get('option4'))

     #Check if nothing was input
    if workout_days_per_week == '' or time_per_workout == '' or fitness_goal == '' or user_experience == '':
        return{
            "statusCode": 400,  # Use the appropriate status code for the error (e.g., 400 for Bad Request)
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps("Please select a value for all options.")
        }

    # Pass the option values as arguments and get the output
    #Return is a dictionary for each workout day (numeric, zero index), then list of each workout for the day
    #Each workout is another list cotaining 3 values - name of the exercise, # of sets, # of reps
    #E.g., {0: [['exercisName#1', set, rep], ['exerciseName#2', set, rep],...}
    output = main(workout_days_per_week, time_per_workout, fitness_goal, user_experience)

    # Check if backend returned an error
    if isinstance(output, str):
        return {
            "statusCode": 500,  # Use the appropriate status code for the error (e.g., 500 for Internal Server Error)
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(output)
        }

    return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps(output)
    }


#---------------END FLASK CODE----------------------------------------