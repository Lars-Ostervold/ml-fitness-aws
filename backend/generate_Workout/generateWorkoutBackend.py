import random
from .exercise_lists import *

def get_split_selection(workout_days_per_week, user_experience):
    split_dict = {}
    if user_experience == 1: #Beginner
        split_dict = {day: [] for day in range(1, workout_days_per_week + 1)} #Initialize the dictionary with the number of days
        #This loop adds a full body workout, which is just chest, back, and legs.
        for i in range(1, workout_days_per_week + 1):
            split_dict[i].append("CHEST")
            split_dict[i].append("BACK")
            split_dict[i].append("LEGS")
        return split_dict

    #Intermediate and Advanced splits (intermediate doesn't have option to pick >5 days)
    #PUSH = CHEST/TRICEP/SHOULDERS
    #PULL = BACK/BICEP/LOWER BACK/TRAPS
    #FIXME: Currently no FOREARM workouts or lower back
    if workout_days_per_week == 2:  # CHEST+BACK, LEGS+SHOULDERS
        split_dict = {1: ["CHEST", "BACK"], 2: ["LEGS", "SHOULDERS"]}
    elif workout_days_per_week == 3:  # PUSH, PULL, LEGS
        split_dict = {1: ["CHEST", "TRICEP", "SHOULDERS"], 2: ["BACK", "BICEP", "LOWER BACK", "TRAPS"], 3: ["QUAD", "HAMSTRING", "CALVES"]}
    elif workout_days_per_week == 4:  # CHEST, BACK, LEGS, SHOULDERS
        split_dict = {1: ["CHEST", "TRICEP"], 2: ["BACK", "BICEP"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["SHOULDERS", "TRICEP"]}
    elif workout_days_per_week == 5:  # CHEST, BACK, LEGS, SHOULDERS, ARMS
        split_dict = {1: ["CHEST", "TRICEP"], 2: ["BACK", "BICEP"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["SHOULDERS", "TRICEP"], 5: ["TRICEP", "BICEP", "FOREARM"]}
    elif workout_days_per_week == 6:  # PUSH, PULL, LEGS, PUSH, PULL, LEGS
        split_dict = {1: ["CHEST", "TRICEP", "SHOULDERS"], 2: ["BACK", "BICEP", "LOWER BACK", "TRAPS"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["CHEST", "TRICEP", "SHOULDERS"], 5: ["BACK", "BICEP", "LOWER BACK", "TRAPS"], 6: ["QUAD", "HAMSTRING", "CALVES"]}
    elif workout_days_per_week == 7:  # PUSH, PULL, LEGS, PUSH, PULL, LEGS, RECOVER
        split_dict = {1: ["CHEST", "TRICEP", "SHOULDERS"], 2: ["BACK", "BICEP", "LOWER BACK", "TRAPS"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["CHEST", "TRICEP", "SHOULDERS"], 5: ["BACK", "BICEP", "LOWER BACK", "TRAPS"], 6: ["QUAD", "HAMSTRING", "CALVES"], 7: ["RECOVER"]}
    else:
        print("ERROR: COULD NOT GENERATE SPLIT in get_split_selection()")
    return split_dict

#Given a split for a day, generate a 'skeleton' workout plan. The skeleton will say what muscle group, whether it's
#a compound or accessory movement, and how many sets/reps to do.
def generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout, add_abs):
    
    daily_workout_skeleton = {}

    #Find the number of sets assuming 2.5 minutes per set
    number_of_sets = int(time_per_workout // 2.5)

    #Given the number_of_sets, we need to figure out how many exercises to do for the day
    #FIXME - This is a hacky way to do this, can improve logic.
    number_of_exercises = int(number_of_sets // 4)
    remainder = number_of_sets % 4
    if remainder > 0:
        number_of_exercises += 1

    #If the user is a beginner, all movements are compound movements. Else, use the logic.
    if user_experience == 1:
        number_of_compound_exercises = len(daily_split)
    else:
        #The first two exercises should always be compound movements. If more than 2, then
        #make sure compound >= accessory
        if number_of_exercises > 2:
            if number_of_exercises % 2 == 0: #Check if even
                number_of_compound_exercises = number_of_exercises // 2
            else:
                number_of_compound_exercises = number_of_exercises // 2 + 1
        else:
            number_of_compound_exercises = number_of_exercises

    #Now I know how many compound and accessory exercises to do. The compounds movements
    #will be the first ones in the list. The rest will be accessory movements. So now 
    #I need to figure out the muscle groups in the daily_split, note compound or accessory,
    #and then assign a set/rep scheme.

    #Let's do this by first assigning compound and accessory to the skeleton, then randomly
    #choosing muscle groups.
    for i in range(number_of_compound_exercises):
        daily_workout_skeleton[i] = ["COMPOUND"]
    for i in range(number_of_compound_exercises, number_of_exercises):
        daily_workout_skeleton[i] = ["ACCESSORY"]

    #Now we need to randomly choose muscle groups from daily_split, but we don't want to repeat muscle groups until all muscle groups have been used
    #But we need repeats if there are more exercises than muscle groups, so we need to check for that.
    if number_of_exercises > len(daily_split):
        # We need repeats, but first make sure every muscle_grpup is chosen once
        chosen_unique_values = random.sample(daily_split, len(daily_split))
        # Fill the skeleton list with the chosen unique values
        for i in range(len(chosen_unique_values)):
            daily_workout_skeleton[i].append(chosen_unique_values[i])
        # Then fill the remaining slots with random choices
        for i in range(len(chosen_unique_values), number_of_exercises):
            daily_workout_skeleton[i].append(random.choice(daily_split))
    else:
        #We don't need repeats, so we need to randomly choose from daily_split without repeats
        #We can do this by randomly choosing an index from daily_split, then popping it from the list
        #so it can't be chosen again.
        for i in range(number_of_exercises):
            index = random.randint(0, len(daily_split)-1)
            daily_workout_skeleton[i].append(daily_split[index])
            daily_split.pop(index)
    
    #Set the minimum or maximum number of reps given the fitness goal
    #fitness_goal is stored as an integer value in App.js code
    if fitness_goal == 1:    
        rep_min, rep_max = 3,5
    elif fitness_goal == 2:
        rep_min, rep_max = 8,12
    elif fitness_goal == 3:
        rep_min, rep_max = 15,20

    #Now we need to assign a set/rep scheme to each exercise, which should be the 3rd value in the list.
    #Let's do this by assuming all exercises will be 3 sets, then randomly choosing which exercises will
    #have 4 or 5 sets. Then we can randomly choose reps for each exercise.
    for i in range(number_of_exercises):
        daily_workout_skeleton[i].append(3)
    
    #Now let's loop through the exercises add add a set until we reach the number_of_sets
    for i in range(number_of_exercises*3, number_of_sets):
        index = random.randint(0, number_of_exercises-1)
        daily_workout_skeleton[index][2] += 1
    #Now randomly assign reps for each exercise
    for i in range(number_of_exercises):    
        daily_workout_skeleton[i].append(random.randint(rep_min,rep_max))
    
    #Now we need to add abs if the user wants to
    if add_abs:
        #Keep formatting the same and but "ABDOMINALS" in the 2nd position.
        #3rd position doesn't matter, but 4th is 5-10 minutes. All abs are accessory in the db.
        daily_workout_skeleton[number_of_exercises] = ["ACCESSORY", "ABDOMINALS", 3, random.randint(5,10)]

    return daily_workout_skeleton

#Given a workout skeleton, select exercises from the exercise data.
#Input is a dictionary with the following format: {key: [compound or accessory, muscle group, number of sets, number of reps]}
#This function will return a list of exercises that match the muscle group and compound or accessory movement, along with the number of sets and reps.
def select_exercises(daily_workout_skeleton, user_experience):
    complete_daily_workout = []
    possible_exercises = {}

    #From the user_exeperience variable, set list of possible exercises
    #TODO: Make sure this logic works to set the string for experience.
    exp_str = ''
    if user_experience == 1:
        exp_str = 'BEGINNER'
    elif user_experience == 2:
        exp_str = 'INTERMEDIATE'
    elif user_experience == 3:
        exp_str = 'ADVANCED'
    else:
        print('ERROR: Could not match user_experience in select_exercises().')


    
    #Loop through the daily_workout_skeleton, find matching workouts in the exercise_db, then pick a random matching exercise
    for i in range(len(daily_workout_skeleton)):
        possible_exercises[i] = []
        for exercise in exercise_db: #exercise is a dictionary
            #if index 0 of a key in daily_workout_skeleton mathces value for key 'type' in exercise_db, and index 1 of a 
            #key in daily_workout_skeleton is in value for key 'muscle_group' in exercise_db, then append
            #the 'variation_group' value to possible_exercises. The comparison should be case insensitive.
            if ( #Code below avoids error with NULL values
                daily_workout_skeleton[i][0].lower() in (exercise['type'].lower() if exercise['type'] else '') and
                daily_workout_skeleton[i][1].lower() in (exercise['muscle_group'].lower() if exercise['muscle_group'] else '') and
                exp_str.lower() not in (exercise['exclude_experience_level'].lower() if exercise['exclude_experience_level'] else '')
            ):
                possible_exercises[i].append(exercise['variation_group'])

    #Need to shuffle the possible_exercises list to avoid bias in random
    for i in range(len(possible_exercises)):
        random.shuffle(possible_exercises[i])

    #Now we have a list of possible exercises for each exercise in the daily_workout_skeleton. We need to randomly choose one.
    #However, need to make sure the same exercise is not chosen twice
    seen_exercises = set()
    for i in range(len(daily_workout_skeleton)):
        try:
            #If abs, need to set a for loop that loops 4th index of daily_workout_skeleton[i] times
            #FIXME: Hacky abs solution. 
            if daily_workout_skeleton[i][1] == 'ABDOMINALS':
                seen_abs = []
                for j in range(int(daily_workout_skeleton[i][3]/2)):
                    exercise = random.choice(possible_exercises[i])
                    while exercise in seen_abs:
                        exercise = random.choice(possible_exercises[i])
                    seen_abs.append(exercise)
                #Don't need to track sets/reps for abs, so just append the seen_exercises to the complete_daily_workout list when complete
                complete_daily_workout.append(seen_abs)
            else:
                exercise = random.choice(possible_exercises[i])
                while exercise in seen_exercises:
                    exercise = random.choice(possible_exercises[i])
                seen_exercises.add(exercise) #Update seen exercise set
                #Add the exercise to the complete_daily_workout list with the sets and reps (append only take 1 arg)
                complete_daily_workout.append(exercise)
                complete_daily_workout[i] = [complete_daily_workout[i], daily_workout_skeleton[i][2], daily_workout_skeleton[i][3]]
        except IndexError:
            error_message = f"Could not find {daily_workout_skeleton[i][0].lower()} {daily_workout_skeleton[i][1].lower()} exercises in our database. Please select a different workout split."
            return error_message
    return complete_daily_workout
    

def main(workout_days_per_week: int, time_per_workout: int, fitness_goal: int, user_experience: int, add_abs: bool):   
    #List of muscle groups:
        #Abs, back, biceps, chest, glutes, hamstrings, quads, shoulders, triceps, lower back
        #Accessories - calves, traps, abductors, adductors, forearms, neck?, rotator cuff
    
    master_workout_list = []
    split_dict = get_split_selection(int(workout_days_per_week), int(user_experience))

    #First, generate a skeleton workout based on the split. Then assign sets and reps. Then fill in the workouts.
    for i in split_dict:
        #generate_workout_skeleton will return a dictionary where the key is the day of the workout, the first value is COMPOUND or ACCESSORY, 
        #the second value is the muscle group, and the 3rd value is sets, 4th is reps.
        daily_workout_skeleton = generate_workout_skeleton(split_dict[i], fitness_goal, user_experience, time_per_workout, add_abs)
        daily_workout = select_exercises(daily_workout_skeleton, int(user_experience))
        #See if daily_workout is a string, which means an error was returned
        if isinstance(daily_workout, str):
            return daily_workout
        master_workout_list.append(daily_workout)
    
    weekly_workout_dict = {i: lst for i, lst in enumerate(master_workout_list)}
    
    return weekly_workout_dict




# TODO: Move test cases to a separate file
###------------------------------------TEST CASES-------------------------------------------------
#Generate tests for the functions
def test_get_split_selection():
    print("TESTING get_split_selection()")
    print("TEST 1: 3 days per week, beginner")
    split_dict = get_split_selection(3, 1)
    print(split_dict)
    print("TEST 2: 4 days per week, intermediate")
    split_dict = get_split_selection(4, 2)
    print(split_dict)
    print("TEST 3: 5 days per week, advanced")
    split_dict = get_split_selection(5, 3)
    print(split_dict)
    print("TEST 4: 6 days per week, advanced")
    split_dict = get_split_selection(6, 3)
    print(split_dict)
    print("TEST 5: 7 days per week, advanced")
    split_dict = get_split_selection(7, 3)
    print(split_dict)
def test_generate_workout_skeleton():
    print("TESTING generate_workout_skeleton()")
    daily_split = ['CHEST', 'BACK', 'LEGS']
    fitness_goal = 1
    user_experience = 1
    time_per_workout = 60
    add_abs = True
    daily_workout_skeleton = generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout, add_abs)
    print(daily_workout_skeleton)
    # Should return a dictionary where each key corresponds to a day (0 to n), and the values are lists of length 4
    # with the format ['COMPOUND' or 'ACCESSORY', muscle group, number of sets, number of reps]
    daily_split = ['BICEP', 'TRICEP', 'SHOULDERS']
    fitness_goal = 2
    user_experience = 2
    time_per_workout = 75
    add_abs = True
    daily_workout_skeleton = generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout, add_abs)
    print(daily_workout_skeleton)
    # Should return a dictionary where each key corresponds to a day (0 to n), and the values are lists of length 4
    # with the format ['COMPOUND' or 'ACCESSORY', muscle group, number of sets, number of reps]
    daily_split = ['CHEST', 'BICEP', 'BACK', 'TRICEP']
    fitness_goal = 3
    user_experience = 3
    time_per_workout = 90
    add_abs = True
    daily_workout_skeleton = generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout, add_abs)
    print(daily_workout_skeleton)
    # Should return a dictionary where each key corresponds to a day (0 to n), and the values are lists of length 4
    # with the format ['COMPOUND' or 'ACCESSORY', muscle group, number of sets, number of reps]
    daily_split = ['LEGS', 'BACK', 'SHOULDERS']
    fitness_goal = 1
    user_experience = 2
    time_per_workout = 55
    add_abs = True
    daily_workout_skeleton = generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout, add_abs)
    print(daily_workout_skeleton)
    # Should return a dictionary where each key corresponds to a day (0 to n), and the values are lists of length 4
    # with the format ['COMPOUND' or 'ACCESSORY', muscle group, number of sets, number of reps]
    daily_split = ['CHEST', 'BACK', 'LEGS', 'BICEP', 'TRICEP', 'SHOULDERS']
    fitness_goal = 2
    user_experience = 3
    time_per_workout = 120
    add_abs = True
    daily_workout_skeleton = generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout, add_abs)
    # Should return a dictionary where each key corresponds to a day (0 to n), and the values are lists of length 4
    # with the format ['COMPOUND' or 'ACCESSORY', muscle group, number of sets, number of reps]
    print(daily_workout_skeleton)
def test_select_exercises():
    print("TESTING select_exercises()")
    daily_workout_skeleton = {0: ['COMPOUND', 'CHEST', 3, 5], 1: ['COMPOUND', 'BACK', 3, 5], 2: ['ACCESSORY', 'TRICEP', 3, 5], 3: ['ACCESSORY', 'BICEP', 3, 5], 4: ['ACCESSORY', 'ABDOMINALS', 3, 10]}
    print(f"DAILY WORKOUT SKELETON: {daily_workout_skeleton}")
    daily_workout = select_exercises(daily_workout_skeleton, 2)
    print(f"DAILY WORKOUT: {daily_workout}") 
def test_main():
    print("TESTING main()")
    print(f"MAIN RETURN: {main(4, 60, 2, 2, True)}")

#-------------------OPTIONS TO RUN TEST CODE-----------------------------------------
# test_get_split_selection()
# test_generate_workout_skeleton()
# test_select_exercises()
# test_main()