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
    workout_days_per_week = data.get('option1')
    time_per_workout = data.get('option2')
    fitness_goal = data.get('option3')
    user_experience = data.get('option4')

     #Check if nothing was input, return error code if blanks
    if workout_days_per_week == '' or time_per_workout == '' or fitness_goal == '' or user_experience == '':
        return{
            "statusCode": 400,  # Use the appropriate status code for the error (e.g., 400 for Bad Request)
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps("Please select a value for all options.")
        }
    
    # Pass the option values from front as arguments and get the output
    output = main(workout_days_per_week, time_per_workout, fitness_goal, user_experience)
 
    #Convert list into dictionary
    dict_output = {i: lst for i, lst in enumerate(output)}
    return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps(dict_output)
    } 
