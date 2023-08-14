#Send w/ 'amplify push -y'
import json
from reroll import main as reroll

#This is the entrypoint for Lambda. If I want to define other httpMethods within this, I can pass
#httpMethod from the frontendthen setup if statements here.
def lambda_handler(event, context):

    newExercise = reroll(event.get('exercise'))
    
    return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps(newExercise)
    }
