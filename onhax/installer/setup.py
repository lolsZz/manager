"""
Core installation logic for Dify automated installer.
"""
import os
import sys
import subprocess
import shutil
import docker
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseInstaller:
    """Base installer class that can be extended for any GitHub project.
    
    Uses project-definition.yaml to map documentation steps to automated actions.
    See PROJECT_AUTOMATION.md for documentation on how this works.
    """
    """Base installer class that can be extended for any GitHub project."""
    def __init__(self, installation_path=None):
        self.installation_path = installation_path or os.path.expanduser('~/project')
        self.client = docker.from_env()
        self.venv_created = False
        self.docker_configured = False
        
    def rollback(self):
        """Revert changes on failure."""
        if self.docker_configured:
            try:
                # Stop and remove containers
                containers = self.client.containers.list(filters={'label': 'project.managed'})
                for container in containers:
                    container.stop()
                    container.remove()
            except Exception as e:
                logger.error(f"Failed to cleanup Docker containers: {e}")
                
        if self.venv_created:
            try:
                venv_path = os.path.join(self.installation_path, 'venv')
                if os.path.exists(venv_path):
                    shutil.rmtree(venv_path)
            except Exception as e:
                logger.error(f"Failed to cleanup virtualenv: {e}")

class DifyInstaller(BaseInstaller):
    """Dify installation automation.
    
    This class implements the installation steps defined in project-definition.yaml,
    which maps directly to setup-instructions.md.
    """
    def __init__(self, installation_path=None):
        self.installation_path = installation_path or os.path.expanduser('~/dify')
        self.client = docker.from_env()
    
    def check_prerequisites(self):
        """Check if all required tools are installed."""
        required_commands = {
            'git': 'Git is not installed. Please install git first.',
            'python3': 'Python 3 is not installed.',
            'node': 'Node.js is not installed.',
            'npm': 'NPM is not installed.',
            'docker': 'Docker is not installed.'
        }
        
        for cmd, msg in required_commands.items():
            if not shutil.which(cmd):
                raise RuntimeError(msg)

    def install_nodejs(self):
        """Install Node.js and npm."""
        from .system import system_manager
        if not system_manager.install_nodejs():
            raise RuntimeError("Failed to install Node.js")

    def setup_python_environment(self):
        """Set up Python virtual environment and install requirements."""
        venv_path = os.path.join(self.installation_path, 'venv')
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
        
        # Activate virtual environment and install requirements
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)

    def setup_docker(self):
        """Set up Docker and required containers."""
        from .system import system_manager
        
        # Install Docker if not present
        if not system_manager.install_docker():
            raise RuntimeError("Failed to install Docker")
        
        # Start and enable Docker service
        if not system_manager.start_service('docker'):
            raise RuntimeError("Failed to start Docker service")
        if not system_manager.enable_service('docker'):
            logger.warning("Failed to enable Docker service on boot")
        
        # Pull required images
        self.client.images.pull('postgres:14')
        self.client.images.pull('redis:6')
        
        # Set up Docker Compose configurations
        compose_file = os.path.join(self.installation_path, 'docker-compose.yml')
        if not os.path.exists(compose_file):
            raise FileNotFoundError(f"Docker Compose file not found at {compose_file}")

    def clone_repository(self):
        """Clone the Dify repository."""
        if not os.path.exists(self.installation_path):
            subprocess.run(['git', 'clone', 'https://github.com/langgenius/dify.git', self.installation_path], check=True)
        else:
            logger.info(f"Directory {self.installation_path} already exists")

    def setup_backend(self):
        """Set up the Dify backend."""
        backend_path = os.path.join(self.installation_path, 'api')
        os.chdir(backend_path)
        
        # Copy environment file
        if not os.path.exists('.env'):
            shutil.copy('.env.example', '.env')
        
        # Install dependencies and run migrations
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        subprocess.run(['flask', 'db', 'upgrade'], check=True)
        
        # Create default admin user
        subprocess.run(['flask', 'user', 'create', '--username', 'admin', '--password', 'password', '--email', 'admin@dify.ai'], check=True)

    def setup_frontend(self):
        """Set up the Dify frontend."""
        web_path = os.path.join(self.installation_path, 'web')
        os.chdir(web_path)
        
        # Copy environment file
        if not os.path.exists('.env'):
            shutil.copy('.env.example', '.env')
        
        # Install dependencies
        subprocess.run(['npm', 'install'], check=True)
        subprocess.run(['npm', 'run', 'build'], check=True)

    def verify_installation(self):
        """Verify the installation is working."""
        # Check if required services are running
        try:
            # Check Docker containers
            containers = self.client.containers.list()
            required_containers = ['postgres', 'redis']
            for container in containers:
                if any(req in container.name for req in required_containers):
                    logger.info(f"Container {container.name} is running")
            
            # Try to connect to the backend
            subprocess.run(['curl', 'http://localhost:5001/api/health'], check=True)
            
            # Try to connect to the frontend
            subprocess.run(['curl', 'http://localhost:3000'], check=True)
            
            return True
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return False

    def install(self):
        """Run the complete installation process."""
        steps = [
            ('Checking prerequisites', self.check_prerequisites),
            ('Installing Node.js', self.install_nodejs),
            ('Setting up Python environment', self.setup_python_environment),
            ('Setting up Docker', self.setup_docker),
            ('Cloning repository', self.clone_repository),
            ('Setting up backend', self.setup_backend),
            ('Setting up frontend', self.setup_frontend),
            ('Verifying installation', self.verify_installation)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"Starting step: {step_name}")
            try:
                step_func()
                logger.info(f"Completed step: {step_name}")
            except Exception as e:
                logger.error(f"Failed at step {step_name}: {str(e)}")
                raise

def main():
    """Run the installer directly."""
    installer = DifyInstaller()
    installer.install()

if __name__ == '__main__':
    main()