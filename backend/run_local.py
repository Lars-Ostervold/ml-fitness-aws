#Send w/ 'amplify push -y'
import json
from flask_cors import CORS
from flask import Flask, jsonify, request
import urllib3
from generate_Workout.generateWorkoutBackend import main
from reroll_Workout.reroll import main as reroll


# BASE_ROUTE = "/workout"
http = urllib3.PoolManager()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route("/workout", methods=['POST']) #This expects JSON data containing the option values from the frontend.
def handle_api_request():
    payload = request.get_json()
    
    data = payload.get('payload')  # Get the JSON data from the request body

    # Extract the values from the data dictionary
    workout_days_per_week = data.get('daysPerWeek')
    time_per_workout = data.get('timePerSession')
    fitness_goal = data.get('fitnessGoal')
    user_experience = data.get('userExperience')
    add_abs = bool(data.get('abs_bool'))

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
    output = main(int(workout_days_per_week), int(time_per_workout), int(fitness_goal), int(user_experience), add_abs)

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

@app.route("/reroll", methods=['POST']) #This expects JSON data containing the option values from the frontend.
def handle_reroll_request():
    payload = request.get_json()
    data = payload.get('payload')
    print(data)
    newExercise = reroll(data.get('exercise'))
    
    return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps(newExercise)
    }

#---------------END FLASK CODE----------------------------------------