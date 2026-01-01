#!/bin/bash
# Personal OS - Mac/Linux Launcher Script

echo ""
echo "========================================"
echo "  Personal OS - Starting..."
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo ""
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    echo ""
    echo "Run: cp .env.example .env"
    echo "Then edit .env with your API keys."
    echo ""
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Run the application
echo ""
echo "Starting Personal OS..."
echo "Press Ctrl+C to stop"
echo ""
python main.py
