#!/bin/bash

# LocalSMS Chatbot - Uninstall Script
echo "🗑️  LocalSMS Chatbot - Uninstall"
echo "================================"
echo ""
echo "⚠️  This will remove the LocalSMS Chatbot and ONLY the dependencies"
echo "   that were installed by this project's install script."
echo "   It will NOT remove software that was already installed before."
echo ""

# Stop any running processes
echo "🛑 Stopping running processes..."
pkill -f "python.*chatbot_sms.py" 2>/dev/null
pkill -f "python.*main.py" 2>/dev/null
sleep 2

# Remove virtual environment
if [ -d "venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf venv
fi

# Remove database
if [ -f "sessions.db" ]; then
    echo "🗑️  Removing database..."
    rm -f sessions.db
fi

# Remove logs
if [ -f "chatbot.log" ]; then
    echo "🗑️  Removing logs..."
    rm -f chatbot.log
fi

# Remove data directory
if [ -d "data" ]; then
    echo "🗑️  Removing data directory..."
    rm -rf data
fi

# Remove logs directory
if [ -d "logs" ]; then
    echo "🗑️  Removing logs directory..."
    rm -rf logs
fi

# Remove Python cache
echo "🗑️  Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Remove tracking files
echo "🗑️  Removing tracking files..."
rm -f .ollama_installed .adb_installed .spacy_installed

# Check what was installed by this project
echo "🔍 Checking what was installed by this project..."

# Check if Ollama was installed by this project
if [ -f ".ollama_installed" ]; then
    echo "🗑️  Removing Ollama (installed by this project)..."
    if command -v ollama &> /dev/null; then
        ollama rm llama3:latest 2>/dev/null
        brew uninstall ollama 2>/dev/null
    fi
    rm -f .ollama_installed
else
    echo "✅ Keeping Ollama (was already installed)"
fi

# Check if ADB was installed by this project
if [ -f ".adb_installed" ]; then
    echo "🗑️  Removing ADB (installed by this project)..."
    brew uninstall android-platform-tools 2>/dev/null
    rm -f .adb_installed
else
    echo "✅ Keeping ADB (was already installed)"
fi

# Check if spaCy model was installed by this project
if [ -f ".spacy_installed" ]; then
    echo "🗑️  Removing spaCy model (installed by this project)..."
    python -m spacy uninstall en_core_web_sm 2>/dev/null
    rm -f .spacy_installed
else
    echo "✅ Keeping spaCy model (was already installed)"
fi

echo ""
echo "✅ Uninstall completed!"
echo ""
echo "📁 Remaining files:"
echo "   - Source code (src/, main.py, chatbot_sms.py)"
echo "   - Scripts (install.sh, run.sh, run_clean.sh, uninstall.sh)"
echo "   - Documentation (README.md, ARCHITECTURE.md)"
echo ""
echo "🗑️  To remove everything: rm -rf /Users/iskaypet/Code/local-sms-chat"