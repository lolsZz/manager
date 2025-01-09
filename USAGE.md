# Dify Installer Usage Guide

The Dify Installer provides two ways to install Dify: through a command-line interface (CLI) or through a web-based interface.

## Command Line Installation

### Basic Installation

```bash
# Install the package
pip install onhax-dify-installer

# Run the installer
dify-install install
```

### Custom Installation Path

```bash
dify-install install --path /custom/path/to/dify
```

### Verification

```bash
dify-install verify
```

## Web-Based Installation

### Starting the Web Interface

```bash
# Method 1: Using the CLI
dify-install install --web

# Method 2: Direct web installer
dify-web-install
```

Then open http://localhost:5000 in your browser to start the installation process.

## Configuration

### Default Configuration Location
The default configuration file is located at `~/.dify/config.json`

### Example Configuration File
```json
{
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
  }
}
```

## Post-Installation

After installation completes:

1. Start the backend server:
```bash
cd ~/dify/api
flask run
```

2. Start the frontend:
```bash
cd ~/dify/web
npm start
```

## Troubleshooting

### Common Issues

1. Node.js Installation Failed
```bash
# Manual installation
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs
```

2. Docker Issues
```bash
# Check Docker service
sudo systemctl status docker

# Start Docker if not running
sudo systemctl start docker
```

3. Permission Issues
```bash
# Fix permissions
sudo chown -R $USER:$USER ~/dify
```

### Getting Help

1. Check the logs:
- CLI logs are in the terminal output
- Web installer logs are in the browser console and installation log panel

2. Run verification:
```bash
dify-install verify
```

3. File an issue on GitHub if you need additional help.