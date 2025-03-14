#!/bin/bash

echo ""
echo "==================================================="
echo "   NBA Lineup Optimizer - Startup Script (Unix)"
echo "==================================================="
echo ""

# Check if Python is installed and version is compatible
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check Python version (need 3.8+ for compatibility)
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "[ERROR] Python 3.8 or higher is required (you have $PYTHON_VERSION)"
    echo "Please upgrade Python and try again"
    exit 1
fi

echo "Using Python $PYTHON_VERSION - Version check passed."
echo ""

# Check if Node.js is installed
echo "Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed or not in PATH"
    echo "Please install Node.js 16 or higher and try again"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v)
NODE_MAJOR=$(echo $NODE_VERSION | cut -c2- | cut -d. -f1)

if [ "$NODE_MAJOR" -lt 16 ]; then
    echo "[ERROR] Node.js 16 or higher is required (you have $NODE_VERSION)"
    echo "Please upgrade Node.js and try again"
    exit 1
fi

echo "Using Node.js $NODE_VERSION - Version check passed."
echo ""

# Check available memory
echo "Checking available memory..."
if command -v free &> /dev/null; then
    FREE_MEM_KB=$(free | grep Mem | awk '{print $7}')
    FREE_MEM_GB=$(echo "scale=1; $FREE_MEM_KB/1024/1024" | bc)
    echo "Available memory: ${FREE_MEM_GB}GB"
    
    if (( $(echo "$FREE_MEM_GB < 2" | bc -l) )); then
        echo "[WARNING] Less than 2GB of free memory available"
        echo "The application may run slowly"
        sleep 5
    fi
else
    echo "[WARNING] Could not determine available memory"
fi

# Clean old log files
echo "Cleaning old log files..."
rm -f backend/backend_log.txt frontend/frontend_log.txt

# Check if ports are available
echo "Checking if required ports are available..."
if command -v lsof &> /dev/null; then
    if lsof -Pi :8001 -sTCP:LISTEN -t &> /dev/null; then
        echo "[ERROR] Port 8001 is already in use"
        echo "Please free up port 8001 and try again"
        exit 1
    fi
    
    if lsof -Pi :3000 -sTCP:LISTEN -t &> /dev/null; then
        echo "[ERROR] Port 3000 is already in use"
        echo "Please free up port 3000 and try again"
        exit 1
    fi
else
    echo "[WARNING] Could not check if ports are available (lsof not installed)"
    echo "If the application fails to start, please ensure ports 8001 and 3000 are free"
fi

# Check if virtual environment exists
echo "Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        echo "Make sure you have the venv module installed (pip3 install virtualenv)"
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

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to upgrade pip, continuing with existing version"
fi

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[WARNING] Some dependencies may not have installed correctly"
    echo "Trying to continue anyway..."
fi

# Verify Django installation
if ! python -c "import django" &> /dev/null; then
    echo "[ERROR] Django installation verification failed"
    echo "Try reinstalling with: pip install django==4.2.10"
    exit 1
fi

# Check and fix database
echo ""
echo "Checking database..."
cd backend
python check_db.py
if [ $? -ne 0 ]; then
    echo "[WARNING] Database check encountered issues"
    echo "Trying to continue anyway..."
fi

# Apply migrations
echo ""
echo "Applying database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to apply migrations"
    cd ..
    exit 1
fi

# Fix data if needed
echo ""
echo "Fixing player data..."
python fix_data.py
if [ $? -ne 0 ]; then
    echo "[WARNING] Data fix encountered issues"
    echo "Trying to continue anyway..."
fi

# Start backend server in background
echo ""
echo "Starting backend server..."
python manage.py runserver 8001 > backend_log.txt 2>&1 &
BACKEND_PID=$!
echo "Backend server started in the background (logs in backend_log.txt)"

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
npm start > frontend_log.txt 2>&1 &
FRONTEND_PID=$!
echo "Frontend server started in the background (logs in frontend_log.txt)"

# Go back to root directory
cd ..

echo ""
echo "==================================================="
echo "   NBA Lineup Optimizer started successfully!"
echo ""
echo "   Backend: http://localhost:8001/api"
echo "   Frontend: http://localhost:3000"
echo ""
echo "   Log files:"
echo "   - backend/backend_log.txt"
echo "   - frontend/frontend_log.txt"
echo "==================================================="
echo ""
echo "The application is now running in the background."
echo "You can close this window and the servers will continue running."
echo "To stop the servers, press Ctrl+C in each terminal or use 'kill $BACKEND_PID $FRONTEND_PID'"
echo ""

# Handle cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

# Wait for user to press Ctrl+C
wait