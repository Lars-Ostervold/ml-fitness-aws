#Send w/ 'amplify push -y'
import json
import random
from generateWorkoutBackend import main


#This is the entrypoint for Lambda. If I want to define other httpMethods within this, I can pass
#httpMethod from the frontendthen setup if statements here.
def handler(event, context):
    response = handle_api_request(event)
    return response

def handle_api_request(data):

    # Extract the values from the data dictionary
    workout_days_per_week = int(data.get('option1'))
    time_per_workout = int(data.get('option2'))
    fitness_goal = int(data.get('option3'))
    user_experience = int(data.get('option4'))

     #Check if nothing was input, return error code if blanks
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
