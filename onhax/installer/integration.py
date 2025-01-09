"""
Integration module for Dify installer components.
"""
import os
import logging
from .setup import DifyInstaller
from .config import Config

logger = logging.getLogger(__name__)

class InstallerIntegration:
    def __init__(self, installation_path=None, config_path=None):
        """Initialize the installer integration."""
        self.config = Config(config_path)
        if installation_path:
            self.config.set('installation_path', installation_path)
        self.installer = DifyInstaller(self.config.get('installation_path'))
        self.progress_callback = None

    def set_progress_callback(self, callback):
        """Set callback for progress updates."""
        self.progress_callback = callback

    def update_progress(self, step, progress, message):
        """Update installation progress."""
        if self.progress_callback:
            self.progress_callback(step, progress, message)
        else:
            logger.info(f"{step} ({progress}%): {message}")

    def run_installation(self):
        """Run the complete installation process."""
        try:
            self.update_progress("Checking prerequisites", 5, "Checking system requirements...")
            self.installer.check_prerequisites()
            
            self.update_progress("Installing Node.js", 15, "Installing Node.js...")
            self.installer.install_nodejs()
            
            self.update_progress("Setting up Python", 30, "Configuring Python environment...")
            self.installer.setup_python_environment()
            
            self.update_progress("Setting up Docker", 45, "Configuring Docker...")
            self.installer.setup_docker()
            
            self.update_progress("Cloning Repository", 60, "Cloning Dify repository...")
            self.installer.clone_repository()
            
            self.update_progress("Configuring Environment", 70, "Setting up environment files...")
            # Generate configuration files
            self.config.generate_env_file(
                os.path.join(self.installer.installation_path, 'api', '.env'),
                'backend'
            )
            self.config.generate_env_file(
                os.path.join(self.installer.installation_path, 'web', '.env'),
                'frontend'
            )
            self.config.generate_docker_compose(
                os.path.join(self.installer.installation_path, 'docker-compose.yml')
            )
            
            self.update_progress("Setting up Backend", 80, "Setting up Dify backend...")
            self.installer.setup_backend()
            
            self.update_progress("Setting up Frontend", 90, "Setting up Dify frontend...")
            self.installer.setup_frontend()
            
            self.update_progress("Verifying Installation", 95, "Performing final checks...")
            if not self.installer.verify_installation():
                raise Exception("Installation verification failed")
                
            self.update_progress("Complete", 100, "Installation completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Installation failed: {str(e)}")
            self.update_progress("Failed", -1, f"Error: {str(e)}")
            try:
                self.installer.rollback()
                self.update_progress("Rollback", -1, "Cleaned up failed installation")
            except Exception as rollback_error:
                logger.error(f"Rollback failed: {rollback_error}")
            raise

def create_installer(installation_path=None, config_path=None):
    """Create a new installer integration instance."""
    return InstallerIntegration(installation_path, config_path)