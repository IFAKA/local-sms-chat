#!/bin/bash

# LocalSMS Chatbot - Installation Script
echo "🤖 LocalSMS Chatbot - Installation"
echo "=================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "📦 Installing pyenv..."
    brew install pyenv
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    source ~/.zshrc
else
    echo "✅ pyenv already installed"
fi

# Check if Python 3.13.5 is installed
if pyenv versions | grep -q "3.13.5"; then
    echo "✅ Python 3.13.5 already installed"
    pyenv global 3.13.5
else
    echo "🐍 Installing Python 3.13.5..."
    pyenv install 3.13.5
    pyenv global 3.13.5
fi

# Create virtual environment
if [ -d "venv" ]; then
    echo "✅ Virtual environment already exists"
else
    echo "🔧 Creating virtual environment..."
    python -m venv venv
fi
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install ollama spacy

# Download spaCy model
echo "🧠 Downloading spaCy NLP model..."
python -m spacy download en_core_web_sm
touch .spacy_installed

# Check if ADB is installed
if command -v adb &> /dev/null; then
    echo "✅ ADB already installed"
else
    echo "📱 Installing ADB..."
    brew install android-platform-tools
    touch .adb_installed
fi

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama already installed"
else
    echo "🤖 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    touch .ollama_installed
fi

# Check if LLaMA 3 model is installed
if ollama list | grep -q "llama3:latest"; then
    echo "✅ LLaMA 3 model already installed"
else
    echo "🧠 Downloading LLaMA 3 model..."
    ollama pull llama3:latest
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Set permissions
echo "🔐 Setting permissions..."
chmod +x run.sh setup_adb.sh uninstall.sh

# Create database
echo "🗄️ Initializing database..."
python -c "
import sqlite3
conn = sqlite3.connect('sessions.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        phone TEXT PRIMARY KEY,
        last_input TEXT,
        context TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print('Database initialized')
"

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "📱 Next steps:"
echo "1. Enable USB debugging on your Android device"
echo "2. Connect your device via USB or set up wireless debugging"
echo "3. Run: ./run.sh"
echo ""
echo "🔗 For ADB commands reference:"
echo "   https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8"
echo ""
echo "🛑 To uninstall: ./uninstall.sh"
echo ""
echo "ℹ️  Note: This installer tracks what it installs to avoid removing"
echo "   software that was already installed before running this script."