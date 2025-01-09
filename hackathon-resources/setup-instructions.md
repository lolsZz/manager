# Dify Development Environment Setup Guide for Ubuntu

## Phase 1: Documentation Discovery and Analysis

### Relevant Technical Documentation Files

1. `/README.md` - Main project documentation
   - **Audience**: General users and developers
   - **Type**: Overview, quick start, and deployment options
   - **Detail Level**: Medium, focuses on basic setup and features

2. `/api/README.md` - Backend API setup instructions
   - **Audience**: Backend developers
   - **Type**: Local development setup
   - **Detail Level**: Basic, needs enhancement for Ubuntu-specific steps

3. `/web/README.md` - Frontend setup instructions
   - **Audience**: Frontend developers
   - **Type**: Local development setup
   - **Detail Level**: Basic with some prerequisites

4. `/docker/README.md` - Docker deployment instructions
   - **Audience**: DevOps and developers
   - **Type**: Docker-based deployment
   - **Detail Level**: Detailed for docker setup

5. `/CONTRIBUTING.md` - Development setup and contribution guidelines
   - **Audience**: Contributors and developers
   - **Type**: Development environment setup and workflow
   - **Detail Level**: Detailed, includes core dependencies and project structure

## Phase 2: Development Environment Setup Procedure

### Prerequisites

1. Update Ubuntu System

```bash
sudo apt update
sudo apt upgrade -y
```

2. Install System Dependencies

```bash
sudo apt install -y build-essential curl wget git
```

### Step 1: Install Node.js

The frontend requires Node.js version 18.x (LTS):

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
# Verify installation
node --version # Should be 18.x
npm --version
```

### Step 2: Install Python

The backend requires Python 3.11.x or 3.12.x. For Ubuntu, Python 3.12 can be installed from a PPA:

```bash
# Add deadsnakes PPA for Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip
# Verify installation
python3.12 --version
```

### Step 3: Install Docker and Docker Compose

Required for running middleware services:

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install -y docker-compose
```

### Step 4: Clone the Repository

```bash
git clone https://github.com/langgenius/dify.git
cd dify
```

### Step 5: Setup Backend (API)

1. Create and activate virtual environment:

```bash
cd api
python3.12 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment:

```bash
cp .env.example .env
# Generate a secret key
openssl rand -base64 42
# Add the generated key to .env file as SECRET_KEY

# Required environment variables:
# - SECRET_KEY: Used for session management (generated above)
# - POSTGRES_HOST: Database host (default: localhost)
# - POSTGRES_DB: Database name (default: dify)
# - POSTGRES_USER: Database user (default: postgres)
# - POSTGRES_PASSWORD: Database password
# See .env.example for all available options
```

4. Start required middleware services:

```bash
cd ../docker
docker-compose -f docker-compose.middleware.yaml up -d
```

5. Initialize database:

```bash
cd ../api
flask db upgrade
flask init
```

6. Start backend server:

```bash
flask run
```

### Step 6: Setup Frontend (Web)

1. Install dependencies:

```bash
cd ../web
npm install
```

2. Configure environment:

```bash
cp .env.example .env
```

3. Start development server:

```bash
npm run dev
```

### Development Workflow

#### Project Structure Overview

The project is split into two main parts:

- Backend (api/): A Flask-based Python application
- Frontend (web/): A Next.js-based TypeScript/React application

#### Backend Development

The backend uses Flask with a well-organized modular structure. The backend server supports auto-reloading when code changes are detected. To enable debug mode, set:

```bash
export FLASK_DEBUG=1
```

The backend code (api/) is organized as follows:

- `constants/` - Constant settings used throughout code base
- `controllers/` - API route definitions and request handling logic
- `core/` - Core application orchestration, model integrations, and tools
- `docker/` - Docker & containerization related configurations
- `events/` - Event handling and processing
- `extensions/` - Extensions with 3rd party frameworks/platforms
- `fields/` - Field definitions for serialization/marshalling
- `libs/` - Reusable libraries and helpers
- `migrations/` - Scripts for database migration
- `models/` - Database models & schema definitions
- `services/` - Specifies business logic
- `storage/` - Private key storage
- `tasks/` - Handling of async tasks and background jobs
- `tests/` - Test suites

### Verification Steps

1. Verify backend is running:

```bash
curl http://localhost:5001/health
# Should return a success response
```

2. Verify frontend is running:

- Open <http://localhost:3000> in your browser
- You should see the Dify login page

3. Verify middleware services:

```bash
docker ps
# Should show running containers for:
# - Redis
# - PostgreSQL
# - Weaviate
# - Minio
```

### Development Tools (Optional)

1. Install development tools for better coding experience:

```bash
# For backend
pip install black flake8 pytest

# For frontend
npm install -g eslint prettier
```

### Troubleshooting

Common issues and solutions:

1. Port conflicts:
   - Check if ports 3000, 5001, and required middleware ports are available
   - Use `lsof -i:PORT` to check for processes using specific ports

2. Permission issues:
   - Ensure proper permissions for Docker: `sudo chmod 666 /var/run/docker.sock`
   - Check file permissions in cloned repository

3. Database connection issues:
   - Verify PostgreSQL is running: `docker ps | grep postgres`
   - Check database credentials in .env file

4. Node.js/npm issues:
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`

### Development Tips

#### Frontend Development

- For frontend development, you can use:

  ```bash
  # Run development server with hot reloading
  npm run dev
  # Run storybook for component development
  npm run storybook
  # Run tests
  npm run test
  # Run linting
  npm run lint
  ```

#### Backend Development

- For backend testing:

  ```bash
  # Run tests
  pytest
  # Run specific test file
  pytest tests/test_file.py
  ```

- Python virtual environment should be activated before running any backend commands
- Backend server runs in debug mode with auto-reloading when FLASK_DEBUG=1

### Contributing Guidelines

1. Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:

```bash
git add .
git commit -m "Description of your changes"
```

3. Push to your fork and create a pull request

### Additional Notes

- The development environment uses hot-reloading for both frontend and backend
- Database migrations are handled automatically during the setup process
- Environment variables can be adjusted in the respective .env files
- For external service integrations (e.g., AWS, Azure), additional configuration may be required
- Check the [installation FAQ](https://docs.dify.ai/learn-more/faq/install-faq) for common issues and troubleshooting steps
