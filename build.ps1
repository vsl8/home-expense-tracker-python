# ============================================
# PowerShell Build Script for Windows
# Alternative to Makefile
# ============================================

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  Home Expense Tracker - Build Commands" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\build.ps1 <command>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Development:" -ForegroundColor Green
    Write-Host "  dev          - Run development server with hot reload"
    Write-Host "  test         - Run unit tests"
    Write-Host "  lint         - Run linting checks"
    Write-Host "  shell        - Open shell in dev container"
    Write-Host ""
    Write-Host "Docker:" -ForegroundColor Green
    Write-Host "  build        - Build Docker image"
    Write-Host "  run          - Run production container"
    Write-Host "  stop         - Stop all containers"
    Write-Host "  logs         - View container logs"
    Write-Host "  clean        - Remove containers, images, volumes"
    Write-Host ""
    Write-Host "Production:" -ForegroundColor Green
    Write-Host "  prod         - Build and run production"
    Write-Host ""
}

function Invoke-Dev {
    Write-Host "Starting development server..." -ForegroundColor Green
    docker-compose --profile dev up expense-tracker-dev
}

function Invoke-DevBuild {
    Write-Host "Building development image..." -ForegroundColor Green
    docker-compose --profile dev build expense-tracker-dev
}

function Invoke-Test {
    Write-Host "Running tests..." -ForegroundColor Green
    docker-compose run --rm expense-tracker-dev python -m pytest tests/ -v --cov=app
}

function Invoke-Lint {
    Write-Host "Running linting..." -ForegroundColor Green
    docker-compose run --rm expense-tracker-dev flake8 app tests
    docker-compose run --rm expense-tracker-dev pylint app
}

function Invoke-Shell {
    Write-Host "Opening shell in container..." -ForegroundColor Green
    docker-compose run --rm expense-tracker-dev /bin/bash
}

function Invoke-Build {
    Write-Host "Building production Docker image..." -ForegroundColor Green
    docker-compose build expense-tracker
}

function Invoke-Run {
    Write-Host "Starting production container..." -ForegroundColor Green
    docker-compose up -d expense-tracker
    Write-Host "Application running at http://localhost:5000" -ForegroundColor Cyan
}

function Invoke-Stop {
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    docker-compose down
}

function Invoke-Logs {
    Write-Host "Showing container logs..." -ForegroundColor Green
    docker-compose logs -f expense-tracker
}

function Invoke-Restart {
    Write-Host "Restarting containers..." -ForegroundColor Yellow
    docker-compose restart expense-tracker
}

function Invoke-Prod {
    Write-Host "Building and running production..." -ForegroundColor Green
    Invoke-Build
    Invoke-Run
}

function Invoke-Clean {
    Write-Host "Cleaning up Docker resources..." -ForegroundColor Yellow
    docker-compose down -v --rmi local
    docker system prune -f
}

function Invoke-CleanAll {
    Write-Host "Cleaning ALL Docker resources..." -ForegroundColor Red
    docker-compose down -v --rmi all
    docker system prune -af
}

function Invoke-LocalDev {
    Write-Host "Starting local development server (without Docker)..." -ForegroundColor Green
    & ".\.venv\Scripts\python.exe" run.py
}

function Invoke-LocalTest {
    Write-Host "Running tests locally (without Docker)..." -ForegroundColor Green
    & ".\.venv\Scripts\python.exe" -m pytest tests/ -v --cov=app
}

# Main switch
switch ($Command.ToLower()) {
    "help"      { Show-Help }
    "dev"       { Invoke-Dev }
    "dev-build" { Invoke-DevBuild }
    "test"      { Invoke-Test }
    "lint"      { Invoke-Lint }
    "shell"     { Invoke-Shell }
    "build"     { Invoke-Build }
    "run"       { Invoke-Run }
    "stop"      { Invoke-Stop }
    "logs"      { Invoke-Logs }
    "restart"   { Invoke-Restart }
    "prod"      { Invoke-Prod }
    "clean"     { Invoke-Clean }
    "clean-all" { Invoke-CleanAll }
    "local-dev" { Invoke-LocalDev }
    "local-test"{ Invoke-LocalTest }
    default     { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help 
    }
}
