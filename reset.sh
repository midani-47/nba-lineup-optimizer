#!/bin/bash

echo "NBA Lineup Optimizer - Reset Data"
echo "============================="
echo ""

# Check if the data directory exists
if [ -d "data" ]; then
    echo "Removing cached data files..."
    rm -rf data/*.csv
    rm -rf data/models/*.joblib
    echo "Data files cleared."
else
    echo "No data directory found. Creating it..."
    mkdir -p data/models
fi

echo ""
echo "Reset complete. Run './start.sh' to start the application with fresh data."
echo "" 