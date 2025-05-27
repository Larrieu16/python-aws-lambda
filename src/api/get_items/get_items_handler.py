import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):

    try:

        user_id = (
            event.get("requestContext", {})
            .get("authorizer", {})
            .get("claims", {})
            .get("sub")
        )

        if not user_id:
            return {"statusCode": 401, "body": json.dumps({"error": "Unauthorized"})}

        response = table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
            & Key("SK").begins_with("ITEM#")
        )

        items = response.get("Items", [])
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"items": items}),
        }

    except Exception as e:
        print(f"Error querying items: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
        }
