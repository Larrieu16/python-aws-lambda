import json
import boto3
import uuid
import os
from datetime import datetime
import re  # Adicionado para validação de data

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])  

def lambda_handler(event, context):
    try:
        # Debug: Log do evento recebido
        print("Received event:", json.dumps(event))
        
        # Tratamento do body (pode vir já parseado pelo API Gateway)
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        else:
            body = event.get("body", {})
        
        name = body.get("name")
        date = body.get("date")
        
        # Validação dos parâmetros
        if not name or not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Both 'name' and 'date' are required."})
            }
        
        if not re.match(r'^\d{8}$', date):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Date must be in YYYYMMDD format."})
            }
        
        
        item_id = str(uuid.uuid4())
        item = {
            "PK": f"LIST#{date}",  
            "SK": f"ITEM#{item_id}",  
            "name": name,
            "status": "todo",
            "createdAt": datetime.utcnow().isoformat(),
            "date": date  # Mantém uma cópia da data como atributo
        }
        
        # Inserção no DynamoDB
        table.put_item(Item=item)
        
        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(item)
        }
        
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format"})
        }
    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }