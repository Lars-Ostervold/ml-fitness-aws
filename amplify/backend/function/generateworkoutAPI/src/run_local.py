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

# #Supabase Client init
# SUPABASE_URL = 'https://nfxcfguxrnsmwfcyuoxf.supabase.co'
# SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5meGNmZ3V4cm5zbXdmY3l1b3hmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODg3NTMyOTEsImV4cCI6MjAwNDMyOTI5MX0.-dfJ9jMpr4tNxciR0wiYow0SS0wUy2Ac_SekEKPwt2s'
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route(BASE_ROUTE, methods=['POST']) #This expects JSON data containing the option values from the frontend.
def handle_api_request():
    payload = request.get_json()
    
    data = payload.get('payload')  # Get the JSON data from the request body

    # Extract the values from the data dictionary
    workout_days_per_week = data.get('option1')
    time_per_workout = data.get('option2')
    fitness_goal = data.get('option3')
    user_experience = data.get('option4')

     #Check if nothing was input
    if workout_days_per_week == '' or time_per_workout == '' or fitness_goal == '' or user_experience == '':
        return{
            "statusCode": 400,  # Use the appropriate status code for the error (e.g., 400 for Bad Request)
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps("Please select a value for all options.")
        }

    # Call your Python script or function to generate the output
    # Pass the option values as arguments and get the output
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


#---------------END FLASK CODE----------------------------------------