from app import app

def handler(event, context):
    return {
        "statusCode": 200,
        "body": "Flask app deployed successfully!"
    }