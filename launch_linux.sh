#!/bin/bash

# Has been tested on Kubuntu

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the virtual environment exists
if [[ ! -d "./venv" ]]; then
    echo "Virtual environment not found. Please create it first using:"
    echo "  python3 -m venv venv"
    exit 1
fi

# Activate the virtual environment
source ./venv/bin/activate

# Install dependencies if not already installed
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Run the application
echo "Launching application..."
python3 main.py
