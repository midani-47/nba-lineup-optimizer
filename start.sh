#!/bin/bash

# Start the NBA Lineup Optimizer application

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists python3; then
  echo "Error: python3 is required but not installed."
  exit 1
fi

if ! command_exists npm; then
  echo "Error: npm is required but not installed."
  exit 1
fi

# Set up the backend
echo "Setting up the backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing backend requirements..."
pip install -r ../requirements.txt

# Apply migrations
echo "Applying database migrations..."
python manage.py migrate

# Load NBA data if needed
if [ ! -f "db.sqlite3" ] || [ "$1" == "--reload-data" ]; then
  echo "Loading NBA data..."
  python manage.py load_nba_data
fi

# Start the backend server in the background
echo "Starting backend server on port 8001..."
python manage.py runserver 8001 &
BACKEND_PID=$!

# Go back to the root directory
cd ..

# Set up the frontend
echo "Setting up the frontend..."
cd frontend

# Install dependencies
echo "Installing frontend dependencies..."
npm install --legacy-peer-deps

# Start the frontend server
echo "Starting frontend server..."
npm start &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
  echo "Shutting down servers..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit 0
}

# Register the cleanup function for script termination
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "NBA Lineup Optimizer is running!"
echo "Backend: http://localhost:8001/api/"
echo "Frontend: http://localhost:3000/"
echo "Press Ctrl+C to stop the servers."
wait 