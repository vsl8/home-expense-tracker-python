#!/bin/bash
# ============================================
# Bash Build Script for Linux/macOS
# Equivalent to build.ps1 for Windows
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${CYAN}============================================${NC}"
    echo -e "${CYAN}  Home Expense Tracker - Build Commands${NC}"
    echo -e "${CYAN}============================================${NC}"
    echo ""
    echo -e "${YELLOW}Usage: ./build.sh <command>${NC}"
    echo ""
    echo -e "${GREEN}Development:${NC}"
    echo "  dev          - Run development server with hot reload"
    echo "  dev-build    - Build development Docker image"
    echo "  test         - Run unit tests"
    echo "  lint         - Run linting checks"
    echo "  shell        - Open shell in dev container"
    echo ""
    echo -e "${GREEN}Docker:${NC}"
    echo "  build        - Build Docker image"
    echo "  run          - Run production container"
    echo "  stop         - Stop all containers"
    echo "  logs         - View container logs"
    echo "  restart      - Restart containers"
    echo "  clean        - Remove containers, images, volumes"
    echo "  clean-all    - Remove ALL Docker resources"
    echo ""
    echo -e "${GREEN}Production:${NC}"
    echo "  prod         - Build and run production"
    echo ""
    echo -e "${GREEN}Local (without Docker):${NC}"
    echo "  local-dev    - Run local development server"
    echo "  local-test   - Run tests locally"
    echo ""
}

invoke_dev() {
    echo -e "${GREEN}Starting development server...${NC}"
    docker-compose --profile dev up expense-tracker-dev
}

invoke_dev_build() {
    echo -e "${GREEN}Building development image...${NC}"
    docker-compose --profile dev build expense-tracker-dev
}

invoke_test() {
    echo -e "${GREEN}Running tests...${NC}"
    docker-compose run --rm expense-tracker-dev python -m pytest tests/ -v --cov=app
}

invoke_lint() {
    echo -e "${GREEN}Running linting...${NC}"
    docker-compose run --rm expense-tracker-dev flake8 app tests
    docker-compose run --rm expense-tracker-dev pylint app
}

invoke_shell() {
    echo -e "${GREEN}Opening shell in container...${NC}"
    docker-compose run --rm expense-tracker-dev /bin/bash
}

invoke_build() {
    echo -e "${GREEN}Building production Docker image...${NC}"
    docker-compose build expense-tracker
}

invoke_run() {
    echo -e "${GREEN}Starting production container...${NC}"
    docker-compose up -d expense-tracker
    echo -e "${CYAN}Application running at http://localhost:5000${NC}"
}

invoke_stop() {
    echo -e "${YELLOW}Stopping containers...${NC}"
    docker-compose down
}

invoke_logs() {
    echo -e "${GREEN}Showing container logs...${NC}"
    docker-compose logs -f expense-tracker
}

invoke_restart() {
    echo -e "${YELLOW}Restarting containers...${NC}"
    docker-compose restart expense-tracker
}

invoke_prod() {
    echo -e "${GREEN}Building and running production...${NC}"
    invoke_build
    invoke_run
}

invoke_clean() {
    echo -e "${YELLOW}Cleaning up Docker resources...${NC}"
    docker-compose down -v --rmi local
    docker system prune -f
}

invoke_clean_all() {
    echo -e "${RED}Cleaning ALL Docker resources...${NC}"
    docker-compose down -v --rmi all
    docker system prune -af
}

invoke_local_dev() {
    echo -e "${GREEN}Starting local development server (without Docker)...${NC}"
    ./.venv/bin/python run.py
}

invoke_local_test() {
    echo -e "${GREEN}Running tests locally (without Docker)...${NC}"
    ./.venv/bin/python -m pytest tests/ -v --cov=app
}

# Main command handler
COMMAND="${1:-help}"

case "${COMMAND,,}" in
    help)
        show_help
        ;;
    dev)
        invoke_dev
        ;;
    dev-build)
        invoke_dev_build
        ;;
    test)
        invoke_test
        ;;
    lint)
        invoke_lint
        ;;
    shell)
        invoke_shell
        ;;
    build)
        invoke_build
        ;;
    run)
        invoke_run
        ;;
    stop)
        invoke_stop
        ;;
    logs)
        invoke_logs
        ;;
    restart)
        invoke_restart
        ;;
    prod)
        invoke_prod
        ;;
    clean)
        invoke_clean
        ;;
    clean-all)
        invoke_clean_all
        ;;
    local-dev)
        invoke_local_dev
        ;;
    local-test)
        invoke_local_test
        ;;
    *)
        echo -e "${RED}Unknown command: ${COMMAND}${NC}"
        show_help
        exit 1
        ;;
esac
