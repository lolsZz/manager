"""Basic usage examples for OnHax."""

from onhax.app import OnHaxApp

def generate_simple_app():
    """Example of generating a simple application."""
    app = OnHaxApp()
    result = app.generate_code("Create a simple Flask hello world application")
    app.save_generated_code(result, "hello_world.py")

def generate_with_custom_config():
    """Example of generating code with custom configuration."""
    from onhax.config import Config
    
    config = Config()
    config.model = "advanced"
    
    app = OnHaxApp(config)
    result = app.generate_code("Create a FastAPI CRUD application")
    app.save_generated_code(result, "crud_app.py")

if __name__ == "__main__":
    generate_simple_app()
    generate_with_custom_config()