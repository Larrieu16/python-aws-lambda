import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        pk = body.get("pk")  # e.g., "20250515"
        item_id = body.get("itemId")  # e.g., "1234-5678"
        new_name = body.get("name")
        new_status = body.get("status")
        new_date = body.get("date")

        if not pk or not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Both 'pk' and 'itemId' are required."}),
            }

        key = {"PK": f"LIST#{pk}", "SK": f"ITEM#{item_id}"}

        # Verifica se o item existe
        existing = table.get_item(Key=key)
        if "Item" not in existing:
            return {"statusCode": 404, "body": json.dumps({"error": "Item not found."})}

        update_expression = []
        expression_attrs = {}
        expression_names = {}

        if new_name:
            update_expression.append("#N = :n")
            expression_attrs[":n"] = new_name
            expression_names["#N"] = "name"  # avoid reserved word conflict

        if new_status:
            update_expression.append("#S = :s")
            expression_attrs[":s"] = new_status
            expression_names["#S"] = "status"

        if new_date:
            update_expression.append("#D = :d")
            expression_attrs[":d"] = new_date
            expression_names["#D"] = "date"

        if not update_expression:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No valid fields provided for update."}),
            }

        result = table.update_item(
            Key=key,
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_attrs,
            ExpressionAttributeNames=expression_names,
            ReturnValues="ALL_NEW",
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Item updated successfully.",
                    "updatedItem": result.get("Attributes", {}),
                }
            ),
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
