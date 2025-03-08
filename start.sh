#!/bin/bash

echo ""
echo "==================================================="
echo "   NBA Lineup Optimizer - Startup Script (Unix)"
echo "==================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed or not in PATH"
    echo "Please install Node.js 16 or higher and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[WARNING] Some dependencies may not have installed correctly"
fi

# Check and fix database
echo ""
echo "Checking database..."
cd backend
python3 check_db.py
if [ $? -ne 0 ]; then
    echo "[WARNING] Database check encountered issues"
fi

# Apply migrations
echo ""
echo "Applying database migrations..."
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to apply migrations"
    cd ..
    exit 1
fi

# Fix data if needed
echo ""
echo "Fixing player data..."
python3 fix_data.py
if [ $? -ne 0 ]; then
    echo "[WARNING] Data fix encountered issues"
fi

# Start backend server in background
echo ""
echo "Starting backend server..."
python3 manage.py runserver 8001 &
BACKEND_PID=$!

# Go back to root directory
cd ..

# Install frontend dependencies
echo ""
echo "Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Running dependency fix script..."
    node fix_dependencies.js
    if [ $? -ne 0 ]; then
        echo "[WARNING] Dependency fix encountered issues"
        echo "Trying standard npm install..."
        npm install --legacy-peer-deps
    fi
else
    echo "Frontend dependencies already installed"
fi

# Start frontend server
echo ""
echo "Starting frontend server..."
npm start &
FRONTEND_PID=$!

# Go back to root directory
cd ..

echo ""
echo "==================================================="
echo "   NBA Lineup Optimizer started successfully!"
echo ""
echo "   Backend: http://localhost:8001/api"
echo "   Frontend: http://localhost:3000"
echo "==================================================="
echo ""
echo "Press Ctrl+C to stop all servers"

# Handle cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

# Wait for user to press Ctrl+C
wait 