#!/bin/bash
# AutoShelf Linux Launcher Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📂 AutoShelf Linux Edition${NC}"
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3 first:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "  Fedora/RHEL:   sudo dnf install python3 python3-pip python3-tkinter" 
    echo "  Arch:          sudo pacman -S python python-pip tk"
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: tkinter is not installed${NC}"
    echo "Please install python3-tkinter:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  Fedora/RHEL:   sudo dnf install python3-tkinter"
    echo "  Arch:          sudo pacman -S tk"
    exit 1
fi

# Install dependencies if needed
if [ ! -f ".venv/bin/activate" ]; then
    echo -e "${YELLOW}Setting up virtual environment...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-linux.txt
    echo -e "${GREEN}Setup complete!${NC}"
else
    source .venv/bin/activate
fi

# Check for notify-send (for notifications)
if ! command -v notify-send &> /dev/null; then
    echo -e "${YELLOW}Warning: notify-send not found. Install libnotify-bin for desktop notifications${NC}"
    echo "  Ubuntu/Debian: sudo apt install libnotify-bin"
    echo "  Fedora/RHEL:   sudo dnf install libnotify"
    echo "  Arch:          sudo pacman -S libnotify"
    echo ""
fi

# Launch AutoShelf
echo -e "${GREEN}Starting AutoShelf GUI...${NC}"
python3 gui_app.py

# Deactivate virtual environment
deactivate