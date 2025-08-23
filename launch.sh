#!/bin/bash
# AI PDF Splitter Pro Launcher Script
# This script ensures proper environment setup and launches the GUI

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the project directory
cd "$DIR"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "🚀 AI PDF Splitter Pro - Starting..."
    echo "📁 Project directory: $DIR"
    echo "🐍 Python environment: $(which python)"
    echo "🔧 Launching modern GUI..."
    echo ""
    
    # Launch the GUI
    python ai_pdf_splitter_gui.py
else
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

