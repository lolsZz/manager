"""Client module for interacting with DeepSeek API."""
from typing import Any, Dict, Optional
import requests

from .config import Config

class DeepSeekClient:
    """Client for interacting with DeepSeek API."""
    
    def __init__(self, config: Config):
        """Initialize the DeepSeek client.
        
        Args:
            config: Configuration instance with API credentials
        """
        self.config = config
        if not config.is_configured:
            raise ValueError("DeepSeek API key not configured")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.deepseek_api_key}",
            "Content-Type": "application/json"
        })
        
    def query(self, prompt: str) -> Dict[str, Any]:
        """Send a query to the DeepSeek API.
        
        Args:
            prompt: The prompt to send to the API
            
        Returns:
            The API response as a dictionary
        """
        response = self.session.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        response.raise_for_status()
        return response.json()