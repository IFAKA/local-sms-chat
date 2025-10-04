#!/bin/bash

# LocalSMS Chatbot - Runner
echo "🤖 LocalSMS Chatbot - Starting"
echo "=============================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./install.sh first"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Set Python version (if pyenv is available)
echo "🐍 Setting Python version..."
if command -v pyenv &> /dev/null; then
    pyenv shell 3.13.5 2>/dev/null || echo "⚠️  pyenv shell not available, using system Python"
else
    echo "⚠️  pyenv not available, using system Python"
fi

# Check dependencies
echo "🔍 Checking dependencies..."
python -c "import ollama" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing ollama. Run ./install.sh first"
    exit 1
fi

python -c "import spacy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing spacy. Run ./install.sh first"
    exit 1
fi

python -c "import sqlite3" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing sqlite3. Run ./install.sh first"
    exit 1
fi

echo "✅ All dependencies available"

# Check ADB connection
echo "📱 Checking ADB connection..."
if adb devices | grep -q "device"; then
    echo "✅ ADB device connected"
else
    echo "❌ No ADB device connected"
    echo "   Please connect your device and enable USB debugging"
    echo "   Or set up wireless debugging"
    exit 1
fi

# Start chatbot
echo "🚀 Starting LocalSMS Chatbot..."
echo "📱 Send SMS with 'CHAT: your message' to test"
echo "🛑 Press Ctrl+C to stop"
echo ""

python main.py