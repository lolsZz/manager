"""
Configuration management for Dify installer.
"""
import os
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "installation_path": "~/dify",
    "backend": {
        "host": "localhost",
        "port": 5001,
        "admin_email": "admin@dify.ai",
        "admin_password": "password"
    },
    "frontend": {
        "host": "localhost",
        "port": 3000
    },
    "database": {
        "type": "postgres",
        "version": "14",
        "host": "localhost",
        "port": 5432,
        "name": "dify",
        "user": "postgres",
        "password": "password"
    },
    "redis": {
        "host": "localhost",
        "port": 6379
    },
    "docker": {
        "compose_file": "docker-compose.yml",
        "network": "dify_network"
    }
}

class Config:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.expanduser('~/.dify/config.json')
        self.config = DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
    
    def save(self):
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value."""
        self.config[key] = value
        self.save()
    
    def update(self, updates):
        """Update multiple configuration values."""
        self.config.update(updates)
        self.save()
    
    def generate_env_file(self, path, type='backend'):
        """Generate environment file for backend or frontend."""
        env_vars = []
        
        if type == 'backend':
            env_vars.extend([
                f"DATABASE_URL=postgresql://{self.config['database']['user']}:{self.config['database']['password']}@{self.config['database']['host']}:{self.config['database']['port']}/{self.config['database']['name']}",
                f"REDIS_URL=redis://{self.config['redis']['host']}:{self.config['redis']['port']}/0",
                "SECRET_KEY=your-secret-key",
                f"ADMIN_EMAIL={self.config['backend']['admin_email']}",
                f"ADMIN_PASSWORD={self.config['backend']['admin_password']}",
                f"PORT={self.config['backend']['port']}"
            ])
        elif type == 'frontend':
            env_vars.extend([
                f"NEXT_PUBLIC_API_URL=http://{self.config['backend']['host']}:{self.config['backend']['port']}",
                f"PORT={self.config['frontend']['port']}"
            ])
        
        env_content = '\n'.join(env_vars)
        with open(path, 'w') as f:
            f.write(env_content)

    def generate_docker_compose(self, path):
        """Generate Docker Compose configuration."""
        compose_config = {
            'version': '3.8',
            'services': {
                'postgres': {
                    'image': f"postgres:{self.config['database']['version']}",
                    'environment': {
                        'POSTGRES_DB': self.config['database']['name'],
                        'POSTGRES_USER': self.config['database']['user'],
                        'POSTGRES_PASSWORD': self.config['database']['password']
                    },
                    'ports': [f"{self.config['database']['port']}:5432"],
                    'volumes': ['postgres_data:/var/lib/postgresql/data']
                },
                'redis': {
                    'image': 'redis:6',
                    'ports': [f"{self.config['redis']['port']}:6379"],
                    'volumes': ['redis_data:/data']
                }
            },
            'volumes': {
                'postgres_data': None,
                'redis_data': None
            },
            'networks': {
                self.config['docker']['network']: {
                    'driver': 'bridge'
                }
            }
        }
        
        with open(path, 'w') as f:
            json.dump(compose_config, f, indent=2)