"""Tests for the Dify installer package."""
import os
import pytest
from onhax.installer.setup import DifyInstaller
from onhax.installer.config import Config
from onhax.installer.integration import create_installer

def test_config_loading():
    """Test configuration loading and saving."""
    config = Config()
    assert config.get('installation_path') == '~/dify'
    
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value'

def test_prerequisites_check(tmpdir):
    """Test prerequisites checking."""
    installer = DifyInstaller(str(tmpdir))
    try:
        installer.check_prerequisites()
    except RuntimeError as e:
        # This is expected if some tools are not installed
        assert 'is not installed' in str(e)

def test_installer_integration(tmpdir):
    """Test installer integration."""
    integration = create_installer(installation_path=str(tmpdir))
    
    def progress_callback(step, progress, message):
        assert progress >= 0 or progress == -1
        assert isinstance(step, str)
        assert isinstance(message, str)
    
    integration.set_progress_callback(progress_callback)

def test_env_file_generation(tmpdir):
    """Test environment file generation."""
    config = Config()
    env_path = tmpdir.join('.env')
    
    config.generate_env_file(str(env_path), 'backend')
    assert env_path.exists()
    
    content = env_path.read()
    assert 'DATABASE_URL=' in content
    assert 'REDIS_URL=' in content

def test_docker_compose_generation(tmpdir):
    """Test Docker Compose file generation."""
    config = Config()
    compose_path = tmpdir.join('docker-compose.yml')
    
    config.generate_docker_compose(str(compose_path))
    assert compose_path.exists()
    
    content = compose_path.read()
    assert 'postgres:' in content
    assert 'redis:' in content