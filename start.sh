#!/bin/bash

# NBA Lineup Optimizer Startup Script
echo "🏀 Starting NBA Lineup Optimizer..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install npm first."
    exit 1
fi

# Set up virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Check if we need to reload data
RELOAD_DATA=false
if [ "$1" == "--reload-data" ]; then
    RELOAD_DATA=true
fi

# Navigate to backend directory
cd backend

# Apply migrations
echo "🔄 Applying database migrations..."
python3 manage.py migrate

# Load data if requested or if database is empty
if [ "$RELOAD_DATA" = true ]; then
    echo "🔄 Reloading NBA data..."
    python3 manage.py load_nba_data
fi

# Fix player data
echo "🔄 Fixing player data..."
python3 fix_data.py

# Start backend server in the background
echo "🚀 Starting backend server..."
python3 manage.py runserver 8001 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Navigate to frontend directory
cd ../frontend

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install --legacy-peer-deps

# Start frontend server
echo "🚀 Starting frontend server..."
npm start &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

echo "✅ NBA Lineup Optimizer is running!"
echo "📊 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8001/api"
echo "Press Ctrl+C to stop both servers."

# Keep script running
wait 