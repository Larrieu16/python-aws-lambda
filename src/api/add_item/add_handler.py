import json
import boto3
import uuid
import os
from datetime import datetime


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])  

def save_item(item):
    table.put_item(Item=item)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        name = body.get("name")
        date = body.get("date")  # Expected format: YYYYMMDD

        if not name or not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Both 'name' and 'date' are required."})
            }

        item_id = str(uuid.uuid4())
        item = {
            "PK": date,
            "SK": item_id,
            "name": name,
            "status": "todo",
            "createdAt": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps(item)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
