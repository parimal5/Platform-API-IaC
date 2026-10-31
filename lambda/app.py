import json

def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "LaunchPad Lambda test successful",
            "event": event
        })
    }