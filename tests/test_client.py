"""Tests for the API client module."""
import pytest
from onhax.client import DeepSeekClient
from onhax.config import Config

def test_client_initialization():
    """Test that client can be initialized."""
    config = Config()
    client = DeepSeekClient(config)
    assert client is not None

@pytest.mark.integration
def test_query():
    """Test API query functionality."""
    config = Config()
    client = DeepSeekClient(config)
    
    result = client.query("Test prompt")
    assert isinstance(result, dict)
    assert "response" in result