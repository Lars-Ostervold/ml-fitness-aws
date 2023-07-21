import random
from exercise_lists import *

def get_split_selection(workout_days_per_week, user_experience):
    split_dict = {}
    if user_experience == 1: #Beginner
        #Make a loop that iterates #of workout days and adds a 'FULL'
        #for each
        #FIXME: 'FULL' currently has no options to pull workouts. Maybe replace with:
        #FIXME: chest, back, legs. But they should all be compound movements.
        for i in range(1, workout_days_per_week + 1):
            split_dict[i] = "FULL"
        return split_dict

    #Intermediate and Advanced splits (intermediate doesn't have option to pick >5 days)
    #PUSH = CHEST/TRICEP/SHOULDERS
    #PULL = BACK/BICEP/LOWER BACK/TRAPS
    #FIXME: Currently no FOREARM workouts
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
def generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout):
    #FIXME: If beginner, change to all compounds movements
    daily_workout_skeleton = {}

    #Find the number of sets assuming 2.5 minutes per set
    number_of_sets = int(time_per_workout // 2.5)

    #Given the number_of_sets, we need to figure out how many exercises to do for the day
    #FIXME - This is a hacky way to do this, can improve logic.
    number_of_exercises = int(number_of_sets // 4)
    remainder = number_of_sets % 4
    if remainder > 0:
        number_of_exercises += 1

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
    #FIXME: Need logic to make sure at least 1 exercises of every muscle group in this.
    #FIXME: Maybe can pop the first round, then random selection
    if number_of_exercises > len(daily_split):
        #We need repeats, so we can just randomly choose from daily_split
        for i in range(number_of_exercises):
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

    return daily_workout_skeleton

#Given a workout skeleton, select exercises from the exercise data.
#Input is a dictionary with the following format: {key: [compound or accessory, muscle group, number of sets, number of reps]}
#This function will return a list of exercises that match the muscle group and compound or accessory movement, along with the number of sets and reps.
def select_exercises(daily_workout_skeleton):
    #FIXME: User experience should be used to filter workouts.
    #FIXME: This needs both a min and max level (advanced users should NEVER be doing kneeling push-ups)
    complete_daily_workout = []
    possible_exercises = {}

    #Loop through the daily_workout_skeleton, find matching workouts in the exercise_db, then pick a random matching exercise
    for i in range(len(daily_workout_skeleton)):
        possible_exercises[i] = []
        for exercise in exercise_db: #exercise is a dictionary
            #if index 0 of a key in daily_workout_skeleton mathces value for key 'type' in exercise_db, and index 1 of a 
            #key in daily_workout_skeleton is in value for key 'muscle_group' in exercise_db, then append
            #the 'variation_group' value to possible_exercises. The comparison should be case insensitive.
            if ( #Code below avoids error with NULL values
                daily_workout_skeleton[i][0].lower() in (exercise['type'].lower() if exercise['type'] else '') and
                daily_workout_skeleton[i][1].lower() in (exercise['muscle_group'].lower() if exercise['muscle_group'] else '')
            ):
                possible_exercises[i].append(exercise['variation_group'])


    #Now we have a list of possible exercises for each exercise in the daily_workout_skeleton. We need to randomly choose one.
    for i in range(len(daily_workout_skeleton)):
        complete_daily_workout.append(random.choice(possible_exercises[i]))
        #now add the sets and reps to the list
        complete_daily_workout[i] = [complete_daily_workout[i], daily_workout_skeleton[i][2], daily_workout_skeleton[i][3]]


    return complete_daily_workout
    

def main(workout_days_per_week, time_per_workout, fitness_goal, user_experience):   
    
    #List of muscle groups:
        #Abs, back, biceps, chest, glutes, hamstrings, quads, shoulders, triceps, lower back
        #Accessories - calves, traps, abductors, adductors, forearms, neck?, rotator cuff
    
    master_workout_list = []

    split_dict = get_split_selection(int(workout_days_per_week), int(user_experience))

    #First, generate a skeleton workout based on the split. Then assign sets and reps. Then fill in the workouts.
    for i in split_dict:
        #generate_workout_skeleton will return a dictionary where the key is the day of the workout, the first value is COMPOUND or ACCESSORY, 
        #the second value is the muscle group, and the 3rd value is sets, 4th is reps.
        daily_workout_skeleton = generate_workout_skeleton(split_dict[i], int(fitness_goal), int(user_experience), int(time_per_workout))
        daily_workout = select_exercises(daily_workout_skeleton)
        master_workout_list.append(daily_workout)
    
    weekly_workout_dict = {i: lst for i, lst in enumerate(master_workout_list)}
    
    return weekly_workout_dict





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
def test_select_exercises():
    print("TESTING select_exercises()")
    daily_workout_skeleton = {0: ['COMPOUND', 'CHEST', 3, 5], 1: ['COMPOUND', 'BACK', 3, 5], 2: ['ACCESSORY', 'TRICEP', 3, 5], 3: ['ACCESSORY', 'BICEP', 3, 5]}
    print(f"DAILY WORKOUT SKELETON: {daily_workout_skeleton}")
    daily_workout = select_exercises(daily_workout_skeleton)
    print(f"DAILY WORKOUT: {daily_workout}")
def test_main():
    print("TESTING main()")
    print(f"MAIN RETURN: {main(4, 60, 2, 3)}")

#-------------------OPTIONS TO RUN TEST CODE-----------------------------------------
# test_get_split_selection()
# test_select_exercises()
# test_main()