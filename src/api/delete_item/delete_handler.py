import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"]) 

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        pk = body.get("pk")       # e.g., "LIST#20250515"
        item_id = body.get("itemId")  # e.g., "ITEM#1234-5678"

        if not pk or not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Both 'pk' and 'itemId' are required."})
            }

        response = table.delete_item(
            Key={
                "PK": f"LIST#{pk}",
                "SK": f"ITEM#{item_id}"
            },
            ReturnValues="ALL_OLD"
        )

        if "Attributes" not in response:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Item already deleted or does not exist."})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item successfully deleted."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
