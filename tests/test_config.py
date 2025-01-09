"""Tests for the configuration module."""
import pytest
from onhax.config import Config

def test_config_initialization():
    """Test that config can be initialized."""
    config = Config()
    assert config is not None

def test_config_is_configured():
    """Test configuration state checking."""
    config = Config()
    assert not config.is_configured()  # Should be false by default