#!/bin/bash

# BESS APM Platform Analysis Tool - Startup Script

echo "🔋 Starting BESS APM Platform Investment Analysis Tool"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Install requirements if they don't exist
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if streamlit is installed successfully
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit installation failed."
    exit 1
fi

echo "🚀 Starting the application..."
echo "The application will open in your web browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Start the Streamlit app
streamlit run app.py
