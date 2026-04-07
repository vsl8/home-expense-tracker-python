# Docker Documentation

Complete guide for building, running, and deploying the Home Expense Tracker application using Docker.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Files Overview](#docker-files-overview)
- [Build Commands](#build-commands)
- [Running the Application](#running-the-application)
- [Development Workflow](#development-workflow)
- [Production Deployment](#production-deployment)
- [Docker Compose Services](#docker-compose-services)
- [Environment Variables](#environment-variables)
- [Volume Management](#volume-management)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher (included with Docker Desktop)

### Installation

**Windows:**
- Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

**macOS:**
- Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)

**Linux:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin
```

---

## Quick Start

### Option 1: Using Build Scripts

**Windows (PowerShell):**
```powershell
# Build and run production
.\build.ps1 prod

# Application will be available at http://localhost:5000
```

**Linux/macOS:**
```bash
# Build and run production
make prod

# Application will be available at http://localhost:5000
```

### Option 2: Using Docker Compose Directly

```bash
# Build the image
docker-compose build

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

---

## Docker Files Overview

| File | Description |
|------|-------------|
| `Dockerfile` | Production multi-stage build with optimized image |
| `Dockerfile.dev` | Development image with hot reload support |
| `docker-compose.yml` | Service orchestration configuration |
| `.dockerignore` | Files excluded from Docker build context |
| `Makefile` | Build automation for Linux/macOS |
| `build.ps1` | Build automation for Windows PowerShell |

### Dockerfile (Production)

The production Dockerfile uses a multi-stage build:

1. **Builder Stage**: Installs dependencies in a virtual environment
2. **Production Stage**: Copies only necessary files, runs as non-root user

Key features:
- Python 3.12 slim base image
- Non-root user for security
- Gunicorn WSGI server
- Built-in health check
- Optimized layer caching

### Dockerfile.dev (Development)

Development Dockerfile includes:
- Flask development server with debug mode
- Hot reload support
- Volume mounts for live code changes

---

## Build Commands

### Windows PowerShell Commands

```powershell
# Show all available commands
.\build.ps1 help

# Build production image
.\build.ps1 build

# Run production container
.\build.ps1 run

# Build and run production
.\build.ps1 prod

# Start development with hot reload
.\build.ps1 dev

# Run tests in container
.\build.ps1 test

# Run linting
.\build.ps1 lint

# View logs
.\build.ps1 logs

# Stop all containers
.\build.ps1 stop

# Clean up resources
.\build.ps1 clean

# Run locally without Docker
.\build.ps1 local-dev
.\build.ps1 local-test
```

### Linux/macOS Make Commands

```bash
# Show all available commands
make help

# Build production image
make build

# Run production container
make run

# Build and run production
make prod

# Start development with hot reload
make dev

# Build development image
make dev-build

# Run tests in container
make test

# Run linting
make lint

# Open shell in container
make shell

# View logs
make logs

# Stop all containers
make stop

# Restart containers
make restart

# Clean up resources
make clean

# Clean ALL Docker resources (use with caution)
make clean-all

# Backup database
make db-backup

# CI/CD build
make ci-build
make ci-test
make ci-lint
```

### Direct Docker Commands

```bash
# Build production image
docker build -t expense-tracker:latest .

# Build development image
docker build -f Dockerfile.dev -t expense-tracker:dev .

# Run production container
docker run -d \
  --name expense-tracker \
  -p 5000:5000 \
  -v expense-data:/app/data \
  expense-tracker:latest

# Run development container
docker run -d \
  --name expense-tracker-dev \
  -p 5000:5000 \
  -v $(pwd)/app:/app/app:ro \
  -v expense-data-dev:/app/data \
  -e FLASK_DEBUG=1 \
  expense-tracker:dev

# Execute command in running container
docker exec -it expense-tracker /bin/bash

# View container logs
docker logs -f expense-tracker

# Stop and remove container
docker stop expense-tracker
docker rm expense-tracker
```

---

## Running the Application

### Production Mode

```bash
# Using docker-compose
docker-compose up -d expense-tracker

# Check status
docker-compose ps

# View logs
docker-compose logs -f expense-tracker

# Access the application
curl http://localhost:5000/health
```

### Development Mode (with Hot Reload)

```bash
# Start development service
docker-compose --profile dev up expense-tracker-dev

# Code changes in ./app/ will automatically reload
```

### Accessing the Application

| Environment | URL |
|-------------|-----|
| Production | http://localhost:5000 |
| Development | http://localhost:5000 |
| Health Check | http://localhost:5000/health |

---

## Development Workflow

### 1. Start Development Container

```bash
# Windows
.\build.ps1 dev

# Linux/macOS
make dev
```

### 2. Make Code Changes

Edit files in the `app/` directory. Changes are automatically detected and the server reloads.

### 3. Run Tests

```bash
# Windows
.\build.ps1 test

# Linux/macOS
make test

# Or directly
docker-compose run --rm expense-tracker-dev python -m pytest tests/ -v --cov=app
```

### 4. Check Code Quality

```bash
# Windows
.\build.ps1 lint

# Linux/macOS
make lint
```

### 5. Open Shell in Container

```bash
# Linux/macOS
make shell

# Or directly
docker-compose run --rm expense-tracker-dev /bin/bash
```

---

## Production Deployment

### Build Production Image

```bash
# Build with docker-compose
docker-compose build expense-tracker

# Or build directly with tag
docker build -t expense-tracker:v1.0.0 .
docker build -t expense-tracker:latest .
```

### Push to Container Registry

```bash
# GitHub Container Registry
docker tag expense-tracker:latest ghcr.io/your-username/expense-tracker:latest
docker push ghcr.io/your-username/expense-tracker:latest

# Docker Hub
docker tag expense-tracker:latest your-username/expense-tracker:latest
docker push your-username/expense-tracker:latest

# Azure Container Registry
docker tag expense-tracker:latest your-registry.azurecr.io/expense-tracker:latest
docker push your-registry.azurecr.io/expense-tracker:latest
```

### Deploy to Server

```bash
# SSH to server and pull image
ssh user@server "docker pull ghcr.io/your-username/expense-tracker:latest"

# Restart container
ssh user@server "docker-compose pull && docker-compose up -d"
```

---

## Docker Compose Services

### Services Defined

| Service | Profile | Description |
|---------|---------|-------------|
| `expense-tracker` | (default) | Production application |
| `expense-tracker-dev` | dev | Development with hot reload |

### Running Specific Services

```bash
# Production only
docker-compose up -d expense-tracker

# Development only
docker-compose --profile dev up expense-tracker-dev

# All services
docker-compose --profile dev up -d
```

---

## Environment Variables

### Application Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `FLASK_DEBUG` | `0` | Enable debug mode (1=true) |
| `SECRET_KEY` | (required) | Flask secret key for sessions |
| `DATABASE_URL` | `sqlite:////app/data/expenses.db` | Database connection string |

### Setting Environment Variables

**Using .env file:**

Create a `.env` file in the project root:

```env
SECRET_KEY=your-super-secret-key-change-in-production
FLASK_ENV=production
DATABASE_URL=sqlite:////app/data/expenses.db
```

**Using docker-compose:**

```bash
# Pass environment variable
SECRET_KEY=mysecret docker-compose up -d

# Or in docker-compose.yml
environment:
  - SECRET_KEY=${SECRET_KEY:-default-dev-key}
```

**Using docker run:**

```bash
docker run -d \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  expense-tracker:latest
```

---

## Volume Management

### Named Volumes

| Volume | Mount Point | Purpose |
|--------|-------------|---------|
| `expense-tracker-data` | `/app/data` | Production database persistence |
| `expense-tracker-data-dev` | `/app/data` | Development database persistence |

### Volume Commands

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect expense-tracker-data

# Backup database
docker cp expense-tracker-app:/app/data/expenses.db ./backup_expenses.db

# Restore database
docker cp ./backup_expenses.db expense-tracker-app:/app/data/expenses.db

# Remove volume (WARNING: deletes data)
docker volume rm expense-tracker-data
```

### Database Backup Script

```bash
# Create timestamped backup
docker cp expense-tracker-app:/app/data/expenses.db \
  ./backup_expenses_$(date +%Y%m%d_%H%M%S).db
```

---

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check logs
docker-compose logs expense-tracker

# Check container status
docker-compose ps

# Rebuild image
docker-compose build --no-cache
```

#### Port Already in Use

```bash
# Check what's using port 5000
# Windows
netstat -ano | findstr :5000

# Linux/macOS
lsof -i :5000

# Use different port
docker-compose up -d -p 8080:5000
```

#### Permission Denied Errors

```bash
# Fix volume permissions (Linux)
sudo chown -R 1000:1000 ./data

# Or run container as root (not recommended for production)
docker run --user root expense-tracker:latest
```

#### Database Not Persisting

```bash
# Ensure volume is mounted
docker inspect expense-tracker-app | grep Mounts -A 20

# Check volume exists
docker volume ls | grep expense
```

#### Hot Reload Not Working (Development)

```bash
# Ensure volume is mounted correctly
docker-compose --profile dev up expense-tracker-dev

# Check file permissions
ls -la app/

# Rebuild dev image
docker-compose --profile dev build expense-tracker-dev
```

### Debug Commands

```bash
# Enter running container
docker exec -it expense-tracker-app /bin/bash

# Check Python environment
docker exec expense-tracker-app python --version
docker exec expense-tracker-app pip list

# Test database connection
docker exec expense-tracker-app python -c "from app import create_app; app = create_app(); print('OK')"

# Check health endpoint
curl http://localhost:5000/health

# View real-time logs
docker-compose logs -f --tail=100
```

### Cleanup Commands

```bash
# Stop all containers
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v

# Remove all unused images
docker image prune -a

# Full cleanup
docker system prune -af --volumes
```

---

## CI/CD Integration

The GitHub Actions workflow automatically:

1. Builds Docker image on push
2. Pushes to GitHub Container Registry
3. Runs security scans with Trivy
4. Deploys to environments (DEV → QA → PROD)

### Pull Image from GitHub Container Registry

```bash
# Authenticate
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull latest
docker pull ghcr.io/your-org/expense-tracker:latest

# Pull specific version
docker pull ghcr.io/your-org/expense-tracker:sha-abc1234
```

---

## Best Practices

1. **Never use `latest` tag in production** - Use specific version tags
2. **Always use secrets for sensitive data** - Don't hardcode in docker-compose
3. **Keep images small** - Use multi-stage builds, slim base images
4. **Run as non-root** - Security best practice
5. **Use health checks** - Enable automatic container recovery
6. **Persist data with volumes** - Don't store data in containers
7. **Pin dependency versions** - Reproducible builds
8. **Scan for vulnerabilities** - Use Trivy or similar tools
