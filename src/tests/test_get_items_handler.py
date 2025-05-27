import json

from api.get_items.get_items_handler import lambda_handler


def test_lambda_handler_success(mock_os_environ, sample_authorized_event, mock_table):
    user_id = sample_authorized_event["requestContext"]["authorizer"]["claims"]["sub"]

    mock_db_items = [
        {
            "PK": f"USER#{user_id}",
            "SK": "ITEM#1",
            "name": "Comprar leite",
            "date": "20250526",
            "status": "todo",
            "createdAt": "2025-05-26T00:00:00Z",
        },
        {
            "PK": f"USER#{user_id}",
            "SK": "ITEM#2",
            "name": "Comprar arroz",
            "date": "20250526",
            "status": "todo",
            "createdAt": "2025-05-26T00:00:00Z",
        },
    ]

    mock_table.query.return_value = {"Items": mock_db_items}

    response = lambda_handler(sample_authorized_event, None)

    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert json.loads(response["body"]) == {"items": mock_db_items}


def test_lambda_handler_unauthorized(mock_os_environ, unauthorized_event, mock_table):
    response = lambda_handler(unauthorized_event, None)

    assert response["statusCode"] == 401
    assert json.loads(response["body"]) == {"error": "Unauthorized"}


def test_lambda_handler_exception(mock_os_environ, sample_authorized_event, mock_table):
    user_id = sample_authorized_event["requestContext"]["authorizer"]["claims"]["sub"]

    mock_table.query.side_effect = Exception("Erro simulado")

    response = lambda_handler(sample_authorized_event, None)

    assert response["statusCode"] == 500
    assert json.loads(response["body"]) == {"error": "Internal Server Error"}
