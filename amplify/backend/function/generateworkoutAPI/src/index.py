import json
from flask_cors import CORS
from flask import Flask, jsonify, request
import awsgi
import urllib3

#Import statements for workout generator code
import random
import math
import pandas as pd
import numpy as np
import os

BASE_ROUTE = "/workout"
http = urllib3.PoolManager()

app = Flask(__name__)
#CORS(app)
#CORS(app, origins=['https://master.d3g6fmblygsjiz.amplifyapp.com'])

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
    print("handler ran")
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
    df = pd.read_excel(os.path.join(os.getcwd(),'Exercise_List.xlsx'))
    #Load first column (muscle group)
    column = df.iloc[:, 0].values
    
    #Lists to store all exercises that match muscle group, split into compound and accessory movements
    t_list_strength = []
    t_list_acc = []

    #If the muscle group is arms, need to search for BICEP and TRICEP and return before
    #the next for loop is reached. See next loop for comments
    if muscle_group == "ARMS":
        t_list_tricep = []
        t_list_bicep = []
        for index, value in enumerate(column):
            if "TRICEP" in str(value).upper():
                t_list_tricep.append(df.iloc[index,2]) 
            elif "BICEP" in str(value).upper():
                t_list_bicep.append(df.iloc[index,2])
        tricep_list = random.sample(t_list_tricep,3)
        bicep_list = random.sample(t_list_bicep, 3)
        return [item for pair in zip(tricep_list, bicep_list) for item in pair]

    #Loop through the muscle group column and store exercises (2nd column)
    #that match the muscle_group key
    for index, value in enumerate(column):
        if muscle_group in str(value).upper():
            if "STRENGTH" in str(df.iloc[index,9]).upper():
                t_list_strength.append(df.iloc[index,2])
            else:
                t_list_acc.append(df.iloc[index,2])
    
    #Pick random exercises
    str_list = random.sample(t_list_strength, 3) #Choose 3 random compound movements
    acc_list = random.sample(t_list_acc, 2) #Choose 2 random accessory movements

    #Sanity check to prevent too many lunge variations
    if muscle_group == "LEGS":
        #Load the exercise types from the Excel sheet
        exercise_types = df.iloc[:, 1].values
        
        #Add the strength and accessory lists together
        t_list = str_list + acc_list
        
        #Run a while loop until there is <= 1 lunge variation
        more_than_one_lunge_BOOL = True
        while more_than_one_lunge_BOOL:
            #Create new list to store the movement groups
            movement_group_list = []
            #Store all names of exercises from Excel
            exercise_names = df.iloc[:,2]
            #Find the row for each exercise in the selected exercises
            for value in t_list:
                row = np.where(exercise_names == value)[0]
                movement_group_list.append(df.iloc[row[0], 1])
            #Sum the number of times 'Lunge' occurs
            int = movement_group_list.count("Lunge")
            #If 'Lunge' occurs less than 2 times, then exist the while,
            #otherwise, reroll the exercises.
            if int < 2:
                more_than_one_lunge_BOOL = False
            else:
                str_list = random.sample(t_list_strength, 3) #Choose 3 random compound movements
                acc_list = random.sample(t_list_acc, 2) #Choose 2 random accessory movements
                t_list = str_list + acc_list
     
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

