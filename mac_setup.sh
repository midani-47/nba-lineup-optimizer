#!/bin/bash

echo "MacOS Setup Helper for NBA Lineup Optimizer"
echo "========================================"
echo ""

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. It's recommended for installing dependencies."
    echo "Visit https://brew.sh to install Homebrew"
    echo ""
    read -p "Do you want to continue without Homebrew? (y/n): " continue_without
    if [[ $continue_without != "y" ]]; then
        exit 1
    fi
else
    echo "Installing required system dependencies..."
    
    # Install libomp (needed for some machine learning packages)
    brew install libomp
    
    # Install other potential dependencies
    brew install cmake
    
    echo "System dependencies installed."
fi

# Run the regular start script
echo ""
echo "Running main startup script..."
chmod +x start.sh
./start.sh 