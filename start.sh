#!/bin/bash

echo "NBA Lineup Optimizer Launcher"
echo "==========================="
echo ""

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH."
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed."
    echo "Please install pip and try again."
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify streamlit installation
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit not found in PATH. Installing directly..."
    pip install streamlit
fi

# Run the application using the full path if needed
echo ""
echo "Starting NBA Lineup Optimizer..."
echo ""
python -m streamlit run app.py

# Deactivate virtual environment when app is closed
deactivate

echo ""
echo "Application closed."