#!/bin/bash

echo "🏨 Hotel Management System - Linux/Mac Launcher"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo

# Install requirements
echo "📦 Installing requirements..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install requirements"
    exit 1
fi

echo "✅ Requirements installed"
echo

# Check if display is available
if [ -z "$DISPLAY" ] && [ "$XDG_SESSION_TYPE" != "wayland" ]; then
    echo "⚠️  No display detected. Running database test instead..."
    echo
    python3 test_database.py
    echo
    echo "💡 To run the GUI application, use a system with display support."
    echo "   For SSH: ssh -X username@hostname"
    exit 0
fi

# Run the application
echo "🚀 Starting Hotel Management System..."
echo "================================================"
python3 main.py

echo
echo "Application closed."
