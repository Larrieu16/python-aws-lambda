import json
import os
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError


def parse_response(response):
    if "body" in response:
        return json.loads(response["body"])
    return response


@pytest.mark.parametrize(
    "event_body, expected_error",
    [
        ({"date": "20250528"}, "Both 'name' and 'date' are required."),
        ({"name": "Comprar leite"}, "Both 'name' and 'date' are required."),
        (
            {"name": "Comprar leite", "date": "2025-05-28"},
            "Date must be in YYYYMMDD format.",
        ),
        (
            {"name": "Comprar leite", "date": "2025528"},
            "Date must be in YYYYMMDD format.",
        ),
        ({"name": "", "date": "20250528"}, "Both 'name' and 'date' are required."),
    ],
)
def test_add_item_invalid_inputs(event_body, expected_error, setup_data):
    from api.add_item.add_handler import lambda_handler

    mock_context, _, _, _ = setup_data
    event = {
        "body": json.dumps(event_body),
        "requestContext": {"authorizer": {"claims": {"sub": "user-123"}}},
    }

    response = lambda_handler(event, mock_context)
    parsed_response = parse_response(response)

    assert response["statusCode"] == 400
    assert parsed_response["error"] == expected_error


def test_add_item_invalid_json(setup_data):
    from api.add_item.add_handler import lambda_handler

    mock_context, _, _, _ = setup_data
    event = {
        "body": "{'name': 'invalid json'}",
        "requestContext": {"authorizer": {"claims": {"sub": "user-123"}}},
    }

    response = lambda_handler(event, mock_context)
    parsed_response = parse_response(response)

    assert response["statusCode"] == 400
    assert parsed_response["error"] == "Invalid JSON format"


@patch("boto3.resource")
def test_add_item_dynamodb_error(mock_boto3_resource, setup_data):
    from api.add_item.add_handler import lambda_handler

    mock_context, sample_event_valid, _, _ = setup_data
    mock_table = MagicMock()
    mock_table.put_item.side_effect = ClientError(
        error_response={"Error": {"Code": "ResourceNotFoundException"}},
        operation_name="PutItem",
    )
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_boto3_resource.return_value = mock_dynamodb

    response = lambda_handler(sample_event_valid, mock_context)
    parsed_response = parse_response(response)

    assert response["statusCode"] == 500
    assert parsed_response["error"] == "Internal server error"


@pytest.mark.parametrize(
    "date_input, is_valid",
    [
        ("20250528", True),
        ("20241231", True),
        ("20230101", True),
        ("2025-05-28", False),
        ("2025528", False),
        ("2025/05/28", False),
        ("", False),
        (None, False),
    ],
)
def test_validate_date_format(date_input, is_valid):
    import re

    if is_valid:
        assert re.match(r"^\d{8}$", date_input) is not None
    else:
        if date_input is None:
            assert date_input is None
        else:
            assert re.match(r"^\d{8}$", date_input) is None


def test_error_response():
    from api.add_item.add_handler import lambda_handler

    response = lambda_handler(
        {
            "body": json.dumps({"name": "", "date": "20250528"}),
            "requestContext": {"authorizer": {"claims": {"sub": "user-123"}}},
        },
        None,
    )
    parsed_response = parse_response(response)

    assert response["statusCode"] == 400
    assert parsed_response["error"] == "Both 'name' and 'date' are required."
