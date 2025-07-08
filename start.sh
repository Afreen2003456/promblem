#!/bin/bash

# Airline Data Insights - Quick Start Script

set -e

echo "🛩️  Airline Data Insights - Quick Start"
echo "=========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists pip; then
    echo "❌ pip is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Parse command line arguments
MODE="dev"
BACKEND_PORT=8000
FRONTEND_PORT=8080
INSTALL_DEPS=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --backend-port)
            BACKEND_PORT="$2"
            shift 2
            ;;
        --frontend-port)
            FRONTEND_PORT="$2"
            shift 2
            ;;
        --no-install)
            INSTALL_DEPS=false
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --mode MODE           Set mode (dev/prod) [default: dev]"
            echo "  --backend-port PORT   Backend port [default: 8000]"
            echo "  --frontend-port PORT  Frontend port [default: 8080]"
            echo "  --no-install         Skip dependency installation"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if ports are available
if port_in_use $BACKEND_PORT; then
    echo "❌ Port $BACKEND_PORT is already in use"
    exit 1
fi

if port_in_use $FRONTEND_PORT; then
    echo "❌ Port $FRONTEND_PORT is already in use"
    exit 1
fi

# Setup backend
echo "Setting up backend..."
cd backend

if [ "$INSTALL_DEPS" = true ]; then
    echo "Installing Python dependencies..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    # Try to activate existing virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
fi

# Set environment variables
export DEBUG=$([ "$MODE" = "dev" ] && echo "true" || echo "false")
export HOST=localhost
export PORT=$BACKEND_PORT

# Start backend in background
echo "Starting backend server on port $BACKEND_PORT..."
python run.py &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:$BACKEND_PORT/health >/dev/null 2>&1; then
        echo "✅ Backend is ready"
        break
    fi
    
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start within 30 seconds"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    
    sleep 1
done

# Go back to root directory
cd ..

# Start frontend
echo "Starting frontend server on port $FRONTEND_PORT..."
cd frontend

if command_exists python3; then
    python3 -m http.server $FRONTEND_PORT &
    FRONTEND_PID=$!
elif command_exists python; then
    python -m http.server $FRONTEND_PORT &
    FRONTEND_PID=$!
else
    echo "❌ Cannot start frontend server: Python not found"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Wait for frontend to be ready
echo "Waiting for frontend to be ready..."
for i in {1..10}; do
    if curl -f http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
        echo "✅ Frontend is ready"
        break
    fi
    
    if [ $i -eq 10 ]; then
        echo "❌ Frontend failed to start within 10 seconds"
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
        exit 1
    fi
    
    sleep 1
done

# Success message
echo ""
echo "🎉 Airline Data Insights is now running!"
echo "=========================================="
echo "Backend:  http://localhost:$BACKEND_PORT"
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo "API Docs: http://localhost:$BACKEND_PORT/docs"
echo ""
echo "Press Ctrl+C to stop the servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo "✅ Servers stopped"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Wait for user to stop
wait 