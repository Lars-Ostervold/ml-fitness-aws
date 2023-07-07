#Send w/ 'amplify push -y'
import json
from flask_cors import CORS
from flask import Flask, jsonify, request
import awsgi
import urllib3
from supabase import create_client, Client
#import supabase

#Import statements for workout generator code
import random
import os

BASE_ROUTE = "/workout"
http = urllib3.PoolManager()

app = Flask(__name__)
CORS(app)


SUPABASE_URL = 'https://nfxcfguxrnsmwfcyuoxf.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5meGNmZ3V4cm5zbXdmY3l1b3hmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODg3NTMyOTEsImV4cCI6MjAwNDMyOTI5MX0.-dfJ9jMpr4tNxciR0wiYow0SS0wUy2Ac_SekEKPwt2s'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route(BASE_ROUTE, methods=['POST']) #This expects JSON data containing the option values from the frontend.
def handle_api_request():
    payload = request.get_json()
    data = payload.get('data')  # Get the JSON data from the request body

    # Extract the values from the data dictionary
    option1_value = data.get('option1')
    option2_value = data.get('option2')
    option3_value = data.get('option3')
    option4_value = data.get('option4')

    # Call your Python script or function to generate the output
    # Pass the option values as arguments and get the output
    output = main(option1_value, option2_value, option3_value, option4_value)

    # Return the output as a JSON response
    #return jsonify(output)
    return json.dumps(output)

#This handler is for awsgi and the lambda functions
def handler(event, context):
    return awsgi.response(app, event, context)
#---------------END FLASK CODE----------------------------------------




#####-----------------------BEGIN WORKOUT GENERATOR CODE------------------------------------

#########-------------KNOWN ISSUES-------------------############
#1. Only one option for splits at the moment
#2. No option for how long you want to spend in the gym
#3. generate_routine function just chooses 3 compounds movements and 2 accessory movements right now

######------------THINGS TO ADD-----------------###########
#1. Add in ab workouts
#2. Add in arms as accessory workouts - e.g., chest day has triceps


#Given a muscle group, generate a workout plan for that day
def generate_routine(muscle_group):
    #Import data for excercises
    exercise_list = load_exercise_list()
    #Lists to store all exercises that match muscle group, split into compound and accessory movements
    t_list_strength = []
    t_list_acc = []

    #If the muscle group is arms, need to search for BICEP and TRICEP and return before
    #the next for loop is reached. See next loop for comments
    if muscle_group == "ARMS":
        t_list_tricep = []
        t_list_bicep = []
        for item in exercise_list:
            if "TRICEP" in str(item['muscle_group']).upper():
                t_list_tricep.append(item['variation_group'])
            elif "BICEP" in str(item['muscle_group']).upper():
                t_list_bicep.append(item['variation_group'])
        tricep_list = random.sample(t_list_tricep,3)
        bicep_list = random.sample(t_list_bicep, 3)
        return [item for pair in zip(tricep_list, bicep_list) for item in pair]

    #Loop through the muscle group column and store exercises (2nd column)
    #that match the muscle_group key
    for item in exercise_list:
        if muscle_group in str(item['muscle_group']).upper():
            if "STRENGTH" in str(item['type']).upper():
                t_list_strength.append(item['variation_group'])
            else:
                t_list_acc.append(item['variation_group'])
    
    #Pick random exercises
    str_list = random.sample(t_list_strength, 3) #Choose 3 random compound movements
    acc_list = random.sample(t_list_acc, 2) #Choose 2 random accessory movements

    #Sanity check to prevent too many lunge variations
    if muscle_group == "LEGS":
        # #Load the exercise types from the Excel sheet
        # #exercise_types = [item[2] for item in exercise_list]
        
        # #Add the strength and accessory lists together
        # t_list = str_list + acc_list
        
        # #Run a while loop until there is <= 1 lunge variation
        # more_than_one_lunge_BOOL = True
        # while more_than_one_lunge_BOOL:
        #     #Create new list to store the movement groups
        #     movement_group_list = []
        #     #Store all names of exercises from Excel
        #     exercise_names = [item['variation_group'] for item in exercise_list]
        #     #Find the row for each exercise in the selected exercises
        #     for value in t_list:
        #         for i, exercise_name in enumerate(exercise_names):
        #             if exercise_name == value:
        #                 movement_group_list.append(exercise_list[i, 1])
        #                 break
        #         #row = np.where(exercise_names == value)[0]
        #         #movement_group_list.append(exercise_list.iloc[row[0], 1])
        #     #Sum the number of times 'Lunge' occurs
        #     int = movement_group_list.count("Lunge")
        #     #If 'Lunge' occurs less than 2 times, then exist the while,
        #     #otherwise, reroll the exercises.
        #     if int < 2:
        #         more_than_one_lunge_BOOL = False
        #     else:
        #         str_list = random.sample(t_list_strength, 3) #Choose 3 random compound movements
        #         acc_list = random.sample(t_list_acc, 2) #Choose 2 random accessory movements
        #         t_list = str_list + acc_list
        str_list = random.sample(t_list_strength, 3) #Choose 3 random compound movements
        acc_list = random.sample(t_list_acc, 2) #Choose 2 random accessory movements
     
    #return the compound and accessory movements lists combined
    return str_list + acc_list
    

def generate_rep_scheme(t_list, fitness_goal, user_experience):
    #Find the number of sets assuming 2.5 minutes per set
    #number_of_sets = math.floor(time_per_workout/2.5)

    #Set the minimum or maximum number of reps given the fitness goal
    #fitness_goal is stored as an integer value in App.js code
    if fitness_goal == 1:    
        rep_min, rep_max = 3,5
    elif fitness_goal == 2:
        rep_min, rep_max = 8,12
    elif fitness_goal == 3:
        rep_min, rep_max = 15,20
    #Set minimum or maximum number of sets given the fitness experience
    #user_experience is stored as an integer value in App.js code
    if user_experience == 1:    
        set_min, set_max = 2,3
    elif user_experience == 2:
        set_min, set_max = 3,4
    elif user_experience == 3:
        set_min, set_max = 4,5

    #Choose how many sets for each exercise
    sets = [random.randint(set_min, set_max) for value in t_list]
    #If rep range is 8-12, prevent odd numbers
    if fitness_goal == 2:
        reps = [random.randrange(rep_min,rep_max,2) for value in t_list]
    else:
        reps = [random.randint(rep_min,rep_max) for value in t_list]
    for i in range(len(t_list)):
        suffix = f" {sets[i]}x{reps[i]}"
        t_list[i] += suffix
    return t_list

def load_exercise_list():
    exercise_list = []
    response = supabase.table('Exercise_List').select("*").execute()
    exercise_list = response.data
    return exercise_list

def main(workout_days_per_week, time_per_workout, fitness_goal, user_experience):
    #This line is temporary to get working version
    master_workout_list = []
    split_selection = 1
    #legs, shoulders, back, chest, arms.
    if split_selection == 1:
        print("You've rolled the 5-Day Rotation Split!")
        split_list = ["LEGS", "SHOULDERS", "BACK", "CHEST", "ARMS"]

    for value in split_list:
        daily_workout = generate_routine(value)
        daily_workout = generate_rep_scheme(daily_workout, int(fitness_goal), int(user_experience))
        master_workout_list.append(daily_workout)
    
    return master_workout_list

