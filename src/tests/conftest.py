import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

os.environ["DYNAMODB_TABLE"] = "test-table"


@pytest.fixture(autouse=True, scope="session")
def setup_environment():
    """Ensure env var is set for the session."""
    assert "DYNAMODB_TABLE" in os.environ
    yield


@pytest.fixture
def mock_table():
    """Patch DynamoDB table access."""
    mock_table = MagicMock()
    with patch("api.get_items.get_items_handler.table", mock_table):
        yield mock_table


@pytest.fixture
def sample_event_context():
    """Provide default event/context."""
    event = {"requestContext": {"authorizer": {"claims": {"sub": "default-user-id"}}}}
    context = None
    return event, context


@pytest.fixture
def sample_authorized_event():
    return {"requestContext": {"authorizer": {"claims": {"sub": "123"}}}}


@pytest.fixture
def unauthorized_event():
    return {"requestContext": {"authorizer": {"claims": {}}}}


@pytest.fixture
def setup_data():
    mock_context = MagicMock()
    mock_context.log = MagicMock()

    sample_event_valid = {
        "body": json.dumps({"name": "Comprar leite", "date": "20250528"}),
        "requestContext": {"authorizer": {"claims": {"sub": "user-123"}}},
    }

    sample_event_parsed_body = {
        "body": {"name": "Comprar pão", "date": "20250529"},
        "requestContext": {"authorizer": {"claims": {"sub": "user-456"}}},
    }

    sample_dynamodb_item = {
        "PK": "USER#user-123",
        "SK": "LIST#20250528#ITEM#12345678-1234-5678-9012-123456789012",
        "item_id": "12345678-1234-5678-9012-123456789012",
        "name": "Comprar leite",
        "status": "todo",
        "createdAt": "2025-05-28T10:00:00",
        "date": "20250528",
    }

    return (
        mock_context,
        sample_event_valid,
        sample_event_parsed_body,
        sample_dynamodb_item,
    )
