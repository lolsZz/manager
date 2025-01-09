"""Main application module for onhax project."""
from typing import Optional

from .config import Config
from .client import DeepSeekClient

class OnHaxApp:
    """Main application class for onhax project."""
    
    def __init__(self):
        """Initialize the OnHax application."""
        self.config = Config()
        self.client = DeepSeekClient(self.config)
    
    def generate_code(self, prompt: str) -> str:
        """Generate code based on the given prompt.
        
        Args:
            prompt: The prompt describing the code to generate
            
        Returns:
            The generated code as a string
        """
        response = self.client.query(prompt)
        # Extract the actual code from the response
        # This might need adjustment based on the actual API response structure
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    def save_generated_code(self, code: str, filename: str) -> None:
        """Save generated code to a file.
        
        Args:
            code: The generated code to save
            filename: The name of the file to save the code to
        """
        with open(filename, 'w') as f:
            f.write(code)