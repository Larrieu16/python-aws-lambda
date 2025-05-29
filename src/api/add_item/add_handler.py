import json
import os
import re
import uuid
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        else:
            body = event.get("body", {})

        name = body.get("name")
        date = body.get("date")

        if not name or not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Both 'name' and 'date' are required."}),
            }

        if not re.match(r"^\d{8}$", date):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Date must be in YYYYMMDD format."}),
            }

        user_id = (
            event.get("requestContext", {})
            .get("authorizer", {})
            .get("claims", {})
            .get("sub")
        )

        if not user_id:
            return {"statusCode": 401, "body": json.dumps({"error": "Unauthorized"})}

        item_id = str(uuid.uuid4())
        item = {
            "PK": f"USER#{user_id}",
            "SK": f"LIST#{date}#ITEM#{item_id}",
            "item_id": item_id,
            "name": name,
            "status": "todo",
            "createdAt": datetime.utcnow().isoformat(),
            "date": date,
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(item),
        }

    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON format"})}
    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
        }
