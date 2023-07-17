import random
from supabase import create_client, Client


#Given a muscle group, generate a workout plan for that day
def generate_routine(muscle_group, all_exercise_data):
    #FIXME - Don't include accessory lifts on times <30?
    #Lists to store all exercises that match muscle group, split into compound and accessory movements
    t_list_strength = []
    t_list_acc = []

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
    

def generate_rep_scheme(daily_workout, fitness_goal, user_experience, time_per_workout):
    
    #Find the number of sets assuming 2.5 minutes per set
    #FIXME - Need to change number of sets to depend on fitness goals and exercises?
    number_of_sets = time_per_workout // 2.5

    #Set the minimum or maximum number of reps given the fitness goal
    #fitness_goal is stored as an integer value in App.js code
    if fitness_goal == 1:    
        rep_min, rep_max = 3,5
    elif fitness_goal == 2:
        rep_min, rep_max = 8,12
    elif fitness_goal == 3:
        rep_min, rep_max = 15,20

    #Choose how many sets for each exercise
    sets = [0] * len(daily_workout) #Make sets the appropriate length

    #FIXME: Zeroes are possible in the workout list, but the while loop
    #was not efficient. Try ChatGPT version. Less elegant but while loops
    #are dangerous to include in the code.
    for _ in range(int(number_of_sets)):
        index = random.randint(0, len(sets)-1)
        sets[index] += 1

    #If rep range is 8-12, prevent odd numbers
    if fitness_goal == 2:
        reps = [random.randrange(rep_min,rep_max,2) for value in daily_workout]
    else:
        reps = [random.randint(rep_min,rep_max) for value in daily_workout]
    
    #Add rep scheme to daily workout, then return
    for i in range(len(daily_workout)):
        suffix = f" {sets[i]}x{reps[i]}"
        daily_workout[i] += suffix
    return daily_workout

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

def get_split_selection(workout_days_per_week, user_experience):
    split_list = []
    if user_experience == 1: #Beginner
        #Make a loop that iterates #of workout days and adds a 'FULL'
        #for each
        for i in range(workout_days_per_week):
            split_list = split_list.append("FULL")

    #Intermediate and Advanced splits
    #FIXME - Break PUSH and PULL into muscle components
    if workout_days_per_week == 2:
        split_list = ["CHEST/BACK", "LEGS/SHOULDERS"]
    elif workout_days_per_week == 3:
        split_list = ["PUSH", "PULL", "LEGS"]
    elif workout_days_per_week == 4:
        split_list = ["CHEST/TRICEP", "BACK/BICEP", "QUAD/HAMSTRING", "SHOULDERS"]
    elif workout_days_per_week == 5:
        split_list = ["CHEST/TRICEP", "BACK/BICEP", "QUAD/HAMSTRING", "SHOULDERS", "TRICEP/BICEP"]
    elif workout_days_per_week == 6:
        split_list = ["PUSH", "PULL", "LEGS", "PUSH", "PULL", "LEGS"]
    elif workout_days_per_week == 7:
        split_list = ["PUSH", "PULL", "LEGS", "PUSH", "PULL", "LEGS", "RECOVER"]

    return split_list

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

    split_list = get_split_selection(workout_days_per_week, user_experience)

    #Call exercise data here so we only access Supabase once.
    all_exercise_data = load_exercise_list()

    for value in split_list:
        daily_workout = generate_routine(value, all_exercise_data)
        daily_workout = generate_rep_scheme(daily_workout, int(fitness_goal), int(user_experience), int(time_per_workout))
        master_workout_list.append(daily_workout)
    
    return master_workout_list