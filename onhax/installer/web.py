"""
Web interface for the Dify installer.
"""
from flask import Flask, render_template, jsonify
import threading
import subprocess
import os
import sys

app = Flask(__name__)

class InstallationManager:
    def __init__(self):
        self.current_step = "Not started"
        self.progress = 0
        self.logs = []
        self.status = "pending"
        self.lock = threading.Lock()

    def update_status(self, step, progress, log_entry):
        with self.lock:
            self.current_step = step
            self.progress = progress
            self.logs.append(log_entry)

    def get_status(self):
        with self.lock:
            return {
                "current_step": self.current_step,
                "progress": self.progress,
                "logs": self.logs,
                "status": self.status
            }

installer = InstallationManager()

@app.route('/')
def home():
    """Render the installation dashboard."""
    return render_template('installer.html')

@app.route('/api/status')
def status():
    """Get current installation status."""
    return jsonify(installer.get_status())

@app.route('/api/config', methods=['POST'])
def save_config():
    """Save installation configuration."""
    config_data = request.get_json()
    config = Config()
    updates = {
        'installation_path': config_data.get('installPath', '~/dify'),
        'backend': {
            'admin_email': config_data.get('adminEmail', 'admin@dify.ai'),
            'admin_password': config_data.get('adminPassword', 'password')
        },
        'database': {
            'password': config_data.get('dbPassword', 'password')
        }
    }
    config.update(updates)
    return jsonify({"status": "success"})

@app.route('/api/start', methods=['POST'])
def start_installation():
    """Start the installation process."""
    def run_installation():
        try:
            from .integration import create_installer
            installer.status = "running"
            dify_installer = create_installer()
            dify_installer.set_progress_callback(installer.progress_callback)
            dify_installer.run_installation()
            installer.status = "complete"
            
            installer.update_status("Complete", 100, "Installation completed successfully!")
            installer.status = "complete"
            
        except Exception as e:
            installer.status = "failed"
            installer.update_status("Failed", -1, f"Error: {str(e)}")
    
    thread = threading.Thread(target=run_installation)
    thread.start()
    return jsonify({"status": "started"})

def main():
    """Run the installer web interface."""
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()