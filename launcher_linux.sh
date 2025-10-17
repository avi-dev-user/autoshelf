#!/bin/bash
# AutoShelf Linux Launcher

echo "📂 AutoShelf - Linux Edition"
echo "Starting cross-platform file organizer..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

# Check tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "⚠️  Installing tkinter..."
    sudo apt update && sudo apt install python3-tk -y || {
        echo "❌ Failed to install tkinter"
        exit 1
    }
fi

# Install dependencies if needed
if [ ! -d "$HOME/.local/lib/python3"*/site-packages/watchdog 2>/dev/null ]; then
    echo "📦 Installing dependencies..."
    pip3 install --user -r requirements_linux.txt || pip3 install --user watchdog python-dateutil
fi

# Run AutoShelf
python3 autoshelf.py