"""Tests for the main application module."""
import pytest
from onhax.app import OnHaxApp

def test_app_initialization():
    """Test that the app can be initialized."""
    app = OnHaxApp()
    assert app is not None

def test_code_generation():
    """Test code generation functionality."""
    app = OnHaxApp()
    result = app.generate_code("Create a simple function")
    assert isinstance(result, str)
    assert len(result) > 0

def test_save_generated_code(tmp_path):
    """Test saving generated code to file."""
    app = OnHaxApp()
    code = "print('Hello, World!')"
    filename = tmp_path / "test.py"
    
    app.save_generated_code(code, str(filename))
    
    assert filename.exists()
    assert filename.read_text() == code