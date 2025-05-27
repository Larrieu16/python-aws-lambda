# conftest.py
import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_os_environ():
    """Fixture para mockar a variável de ambiente DYNAMODB_TABLE."""
    with patch.dict(
        os.environ, {"DYNAMODB_TABLE": "test-table"}, clear=True
    ) as patched_env:
        yield patched_env


@pytest.fixture
def mock_table():
    """Fixture para mockar o boto3.resource e o cliente DynamoDB."""
    with patch("boto3.resource") as mock_resource_constructor:
        mock_dynamodb_resource = MagicMock()
        mock_table = MagicMock()

        mock_resource_constructor.return_value = mock_dynamodb_resource
        mock_dynamodb_resource.Table.return_value = mock_table

        yield mock_table


@pytest.fixture
def sample_event_context():
    """Fixture para fornecer um event e context básicos."""
    event = {
        "requestContext": {
            "authorizer": {
                "claims": {
                    "sub": "default-user-id"  # Pode ser sobrescrito no teste se necessário
                }
            }
        }
    }
    context = None
    return event, context


@pytest.fixture
def sample_authorized_event():
    """Fixture para um evento autorizado com um user_id específico."""
    return {"requestContext": {"authorizer": {"claims": {"sub": "123"}}}}


@pytest.fixture
def unauthorized_event():
    """Evento sem 'sub' (user_id)."""
    return {"requestContext": {"authorizer": {"claims": {}}}}
