"""Configuration module for onhax project."""
import os
from typing import Optional

class Config:
    """Configuration class for onhax project."""
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        self.deepseek_api_key: str = os.getenv('DEEPSEEK_API_KEY', '')
        
    @property
    def is_configured(self) -> bool:
        """Check if all required configuration is set."""
        return bool(self.deepseek_api_key)