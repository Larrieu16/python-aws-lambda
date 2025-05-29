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
    """Fixture para garantir que a variável de ambiente esteja definida para toda a sessão de teste."""
    assert "DYNAMODB_TABLE" in os.environ
    yield


@pytest.fixture
def mock_table():
    """Fixture para mockar o boto3.resource e o cliente DynamoDB."""
    # Criar um mock para a tabela
    mock_table = MagicMock()

    # Patch diretamente o objeto table no módulo get_items_handler
    with patch("api.get_items.get_items_handler.table", mock_table):
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