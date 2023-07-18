import random
from supabase import create_client, Client

def get_split_selection(workout_days_per_week, user_experience):
    split_dict = {}
    if user_experience == 1: #Beginner
        #Make a loop that iterates #of workout days and adds a 'FULL'
        #for each
        for i in range(1, workout_days_per_week + 1):
            split_dict[i] = "FULL"

    #Intermediate and Advanced splits
    #PUSH = CHEST/TRICEP/SHOULDERS
    #PULL = BACK/BICEP/LBACK/TRAPS
    if workout_days_per_week == 2:  # CHEST+BACK, LEGS+SHOULDERS
        split_dict = {1: ["CHEST", "BACK"], 2: ["LEGS", "SHOULDERS"]}
    elif workout_days_per_week == 3:  # PUSH, PULL, LEGS
        split_dict = {1: ["CHEST", "TRICEP", "SHOULDERS"], 2: ["BACK", "BICEP", "LBACK", "TRAPS"], 3: ["QUAD", "HAMSTRING", "CALVES"]}
    elif workout_days_per_week == 4:  # CHEST, BACK, LEGS, SHOULDERS
        split_dict = {1: ["CHEST", "TRICEP"], 2: ["BACK", "BICEP"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["SHOULDERS", "TRICEP"]}
    elif workout_days_per_week == 5:  # CHEST, BACK, LEGS, SHOULDERS, ARMS
        split_dict = {1: ["CHEST", "TRICEP"], 2: ["BACK", "BICEP"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["SHOULDERS", "TRICEP"], 5: ["TRICEP", "BICEP", "FOREARM"]}
    elif workout_days_per_week == 6:  # PUSH, PULL, LEGS, PUSH, PULL, LEGS
        split_dict = {1: ["CHEST", "TRICEP", "SHOULDERS"], 2: ["BACK", "BICEP", "LBACK", "TRAPS"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["CHEST", "TRICEP", "SHOULDERS"], 5: ["BACK", "BICEP", "LBACK", "TRAPS"], 6: ["QUAD", "HAMSTRING", "CALVES"]}
    elif workout_days_per_week == 7:  # PUSH, PULL, LEGS, PUSH, PULL, LEGS, RECOVER
        split_dict = {1: ["CHEST", "TRICEP", "SHOULDERS"], 2: ["BACK", "BICEP", "LBACK", "TRAPS"], 3: ["QUAD", "HAMSTRING", "CALVES"], 4: ["CHEST", "TRICEP", "SHOULDERS"], 5: ["BACK", "BICEP", "LBACK", "TRAPS"], 6: ["QUAD", "HAMSTRING", "CALVES"], 7: ["RECOVER"]}

    return split_dict

#Given a split for a day, generate a 'skeleton' workout plan. The skeleton will say what muscle group, whether it's
#a compound or accessory movement, and how many sets/reps to do.
def generate_workout_skeleton(daily_split, fitness_goal, user_experience, time_per_workout):
    
    daily_workout_skeleton = {}

    #Find the number of sets assuming 2.5 minutes per set
    number_of_sets = time_per_workout // 2.5

    #Given the number_of_sets, we need to figure out how many exercises to do for the day
    #FIXME - This is a hacky way to do this, can improve logic.
    number_of_exercises = number_of_sets // 4
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

#Given a muscle group, generate a workout plan for that day
def generate_routine(muscle_group, all_exercise_data):
    #FIXME - Don't include accessory lifts on times <30?
    #Lists to store all exercises that match muscle group, split into compound and accessory movements
    t_list_strength = []
    t_list_acc = []

    #muscle_group is a list of muscle groups, passed from the split_dict function.
    #for each muscle in muscle group, we need to loop through the exercise data and store
    #matches in the appropriate list. From there, we have to select exercises, but we have to make sure
    #that we find at least one movement for each muscle group.
    #FIXME - Need to add a check to make sure that the same exercise isn't selected twice.
    for muscle in muscle_group:
        for item in all_exercise_data:
            if muscle in str(item['muscle_group']).upper():
                if "STRENGTH" in str(item['type']).upper():
                    t_list_strength.append(item['variation_group'])
                else:
                    t_list_acc.append(item['variation_group'])

    #Need to figure out how many exercises to include. Let's use the logic that we 
    #want include new exercises if the numbers of sets / exercises is > 4. So we go total
    #divided by 4, and then round up to the nearest integer.




    #If the muscle group is arms, need to search for BICEP and TRICEP and return before
    #the next for loop is reached. See next loop for comments
    if muscle_group == "ARMS":
        t_list_tricep = []
        t_list_bicep = []
        for item in all_exercise_data:
            if "TRICEP" in str(item['muscle_group']).upper():
                t_list_tricep.append(item['variation_group'])
            elif "BICEP" in str(item['muscle_group']).upper():
                t_list_bicep.append(item['variation_group'])
        tricep_list = random.sample(t_list_tricep,3)
        bicep_list = random.sample(t_list_bicep, 3)
        return [item for pair in zip(tricep_list, bicep_list) for item in pair]

    #Loop through the muscle group column and store exercises (2nd column)
    #that match the muscle_group key
    for item in all_exercise_data:
        if muscle_group in str(item['muscle_group']).upper():
            if "STRENGTH" in str(item['type']).upper():
                t_list_strength.append(item['variation_group'])
            else:
                t_list_acc.append(item['variation_group'])
    
    #Pick random exercises
    str_list = random.sample(t_list_strength, 3) #Choose 3 random compound movements
    acc_list = random.sample(t_list_acc, 2) #Choose 2 random accessory movements

    #Sanity check to prevent too many lunge variations
    #FIXME - The code to avoid lots of lunges doesn't work after switch to supabase.
    if muscle_group == "LEGS":
        # #Load the exercise types from the Excel sheet
        # #exercise_types = [item[2] for item in all_exercise_data]
        
        # #Add the strength and accessory lists together
        # t_list = str_list + acc_list
        
        # #Run a while loop until there is <= 1 lunge variation
        # more_than_one_lunge_BOOL = True
        # while more_than_one_lunge_BOOL:
        #     #Create new list to store the movement groups
        #     movement_group_list = []
        #     #Store all names of exercises from Excel
        #     exercise_names = [item['variation_group'] for item in all_exercise_data]
        #     #Find the row for each exercise in the selected exercises
        #     for value in t_list:
        #         for i, exercise_name in enumerate(exercise_names):
        #             if exercise_name == value:
        #                 movement_group_list.append(all_exercise_data[i, 1])
        #                 break
        #         #row = np.where(exercise_names == value)[0]
        #         #movement_group_list.append(all_exercise_data.iloc[row[0], 1])
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
    

def load_exercise_list():
    #Supabase Client init
    SUPABASE_URL = 'https://nfxcfguxrnsmwfcyuoxf.supabase.co'
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5meGNmZ3V4cm5zbXdmY3l1b3hmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODg3NTMyOTEsImV4cCI6MjAwNDMyOTI5MX0.-dfJ9jMpr4tNxciR0wiYow0SS0wUy2Ac_SekEKPwt2s'
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    exercise_list = []

    # #Get data from Supabase and store in dict 
    response = supabase.table('Exercise_List').select("*").execute()
    exercise_list = response.data

    return exercise_list

def main(workout_days_per_week, time_per_workout, fitness_goal, user_experience):
    #FIXME
    #Based on the split, we should trigger possible muscle groups to include in the lift
        #We can add some optimization to make sure we don't load up 7 hamstring lifts later
    #Then, with the same logic, it would be easy to let the user select the muscle groups instead.
    #This allows the advanced users to customize.
    
    #List of muscle groups:
        #Abs, back, biceps, chest, glutes, hamstrings, quads, shoulders, triceps, lower back
        #Accessories - calves, traps, abductors, adductors, forearms, neck?, rotator cuff
    
    master_workout_list = []

    split_dict = get_split_selection(workout_days_per_week, user_experience)

    #Call exercise data here so we only access Supabase once.
    all_exercise_data = load_exercise_list()

    #First, generate a skeleton workout based on the split. Then assign sets and reps. Then fill in the workouts.
    for i in split_dict:
        #generate_workout_skeleton will return a dictionary where the key is the day of the workout, the first value is COMPOUND or ACCESSORY, 
        #the second value is the muscle group, and the 3rd value is sets, 4th is reps.
        daily_workout = generate_workout_skeleton(split_dict[i], int(fitness_goal), int(user_experience), int(time_per_workout))

        daily_workout = generate_routine(daily_workout, all_exercise_data)
        master_workout_list.append(daily_workout)
    
    return master_workout_list