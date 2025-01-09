#!/bin/bash

# Dify Development Environment Setup Script for Ubuntu
# This script automates the installation process described in UBUNTU_DEV_SETUP.md

set -e  # Exit on error

# Function to check command status
check_status() {
    if [ $? -eq 0 ]; then
        echo "✅ $1 successful"
    else
        echo "❌ $1 failed"
        exit 1
    fi
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "🚀 Starting Dify Development Environment Setup..."

# Check system requirements
echo "Checking system requirements..."
if ! command_exists git; then
    sudo apt-get update
    sudo apt-get install -y git
    check_status "Git installation"
fi

# Check if script is run as root
if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run this script as root"
    exit 1
fi

# Step 1: Install Node.js
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
npm --version

# Step 2: Install Python
echo "Installing Python..."
sudo apt-get update
sudo apt-get install -y python3.10 python3-pip python3.10-venv
python3 --version
pip3 --version

# Step 3: Install Docker and Docker Compose
echo "Installing Docker and Docker Compose..."
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER

# Step 4: Clone Repository
echo "Cloning Dify repository..."
git clone https://github.com/langgenius/dify.git
cd dify

# Step 5: Setup Backend
echo "Setting up backend..."
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
check_status "Backend dependencies installation"

# Configure environment
cp .env.example .env
echo "Generating SECRET_KEY..."
SECRET_KEY=$(openssl rand -base64 42)
sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
check_status "Environment configuration"

# Start middleware services
cd ../docker
echo "Starting middleware services..."
docker-compose -f docker-compose.middleware.yaml up -d
check_status "Middleware services startup"

# Initialize database
cd ../api
echo "Initializing database..."
flask db upgrade
check_status "Database upgrade"
flask init
check_status "Database initialization"

# Create default admin user if not exists
if [ -z "$(flask user list 2>/dev/null | grep admin@dify.ai)" ]; then
    echo "Creating default admin user..."
    flask user create --username admin --password admin --email admin@dify.ai --role admin
    check_status "Admin user creation"
fi

echo "Please configure your .env file in the api directory before continuing."
echo "Once configured, start the backend with: flask run"

# Step 6: Setup Frontend
echo "Setting up frontend..."
cd ../web
cp .env.example .env
npm install
echo "Once backend is configured and running, start the frontend with: npm run dev"

echo """
✨ Installation complete! ✨

To start Dify:
1. Configure your database in api/.env file
2. Start the backend:
   cd api
   source .venv/bin/activate
   flask run

3. Start the frontend (in a new terminal):
   cd web
   npm run dev

For more details, please refer to UBUNTU_DEV_SETUP.md
"""