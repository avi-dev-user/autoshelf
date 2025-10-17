# AutoShelf 📂 - Cross-Platform Edition

<p align="center">
  <img src="logo.png" alt="AutoShelf Logo" width="200">
</p>

> Smart file organization for **macOS** and **Linux**. No AI. No setup. Just works.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![macOS](https://img.shields.io/badge/macOS-11.0+-blue.svg)](https://www.apple.com/macos/)
[![Linux](https://img.shields.io/badge/Linux-Ubuntu%2C%20Debian%2C%20Fedora-green.svg)](https://www.linux.org/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Automatically organize your Downloads folder by file type, size, and date. **Cross-platform** support with native interfaces for each OS.

## ✨ What's New in Cross-Platform Edition

- 🍎 **macOS**: Original menu bar interface (unchanged)
- 🐧 **Linux**: Beautiful GUI interface with modern design
- 🔄 **Auto-detection**: Automatically chooses the right interface
- 🎯 **Same features**: File organization works identically on both platforms

---

## Quick Start

### Option 1: Universal Launcher (Recommended)

```bash
# Clone repository
git clone https://github.com/AmirMGhanem/autoshelf.git
cd autoshelf

# Install dependencies (cross-platform)
pip install -r requirements-cross-platform.txt

# Run (auto-detects your OS)
python3 autoshelf.py
```

### Option 2: Platform-Specific Instructions

#### 🍎 **For macOS Users**

1. **Download for macOS**: [AutoShelf-Installer.dmg](https://github.com/AmirMGhanem/autoshelf/releases/download/v0.1/AutoShelf-Installer.dmg)
2. Install to Applications folder
3. Launch from Applications or use the source:

```bash
# From source (macOS)
pip install -r requirements.txt
python main.py  # Menu bar interface
```

#### 🐧 **For Linux Users**

```bash
# Install dependencies
pip install -r requirements_linux.txt

# Ubuntu/Debian: Install tkinter if needed
sudo apt update && sudo apt install python3-tk

# Run with GUI interface
python3 gui_app.py

# OR use the universal launcher
python3 autoshelf.py
```

**Easy Linux Setup:**
```bash
# Make launcher executable
chmod +x launcher_linux.sh

# Run setup and launch
./launcher_linux.sh
```

---

## 🎛️ Interface Previews

### macOS - Menu Bar Interface
- Native macOS menu bar integration
- System notifications
- Follows macOS design guidelines
- Minimal and unobtrusive

### Linux - Modern GUI Interface
- Clean, modern tkinter-based UI
- Desktop notifications
- Tabbed organization options
- Native Linux look and feel

---

## Organization Methods

**By File Type** (10 categories)
- `images/`, `videos/`, `documents/`, `spreadsheets/`, `presentations/`
- `archives/`, `software/`, `code/`, `audio/`, `others/`

**By File Size**
- `small/` (< 1MB), `medium/` (1-50MB), `large/` (> 50MB)

**By Date Added**
- Monthly folders: `10-2025/`, `09-2025/`, etc.

**Combine Methods** for nested organization:
```
images/small/10-2025/photo.jpg
documents/medium/09-2025/report.pdf
videos/large/10-2025/movie.mp4
```

## 🚀 Features

### Core Features (All Platforms)
- ✅ Real-time file monitoring
- ✅ Smart file categorization
- ✅ Configurable organization methods
- ✅ Works offline (no API keys needed)
- ✅ Handles duplicate files intelligently
- ✅ Preserves file integrity

### Platform-Specific Features

#### macOS
- 🍎 Native menu bar integration
- 🔔 Native macOS notifications
- 🎨 Follows macOS Human Interface Guidelines
- 📱 System tray icon with quick access

#### Linux  
- 🐧 Modern GUI with clean design
- 🔔 Desktop notifications (notify-send)
- 🖥️ Desktop launcher integration
- 🎨 Responsive interface design

---

## 🔧 Platform Requirements

### macOS
- macOS 11.0+ (Big Sur or newer)
- Python 3.9+
- Dependencies: `rumps`, `pync`, `pyobjc-*`

### Linux
- Any modern Linux distribution
- Python 3.9+
- `tkinter` (usually pre-installed)
- `notify-send` for notifications (optional)
- Dependencies: `watchdog`, `python-dateutil`

### Tested Distributions
- ✅ Ubuntu 20.04+
- ✅ Debian 11+
- ✅ Fedora 35+
- ✅ Arch Linux
- ✅ Pop!_OS 21.04+

---

## 📥 Installation Options

### Method 1: Universal (Auto-Detection)
```bash
# Install cross-platform dependencies
pip install -r requirements-cross-platform.txt

# Run universal launcher
python3 autoshelf.py
```

### Method 2: macOS Native
```bash
pip install -r requirements.txt
python main.py
```

### Method 3: Linux Native
```bash
pip install -r requirements_linux.txt
python3 gui_app.py
```

### Method 4: Linux Quick Setup
```bash
chmod +x launcher_linux.sh
./launcher_linux.sh
```

---

## 🎮 Usage Examples

### Basic Usage
```bash
# Start with auto-detection
python3 autoshelf.py

# Platform-specific launches
python main.py      # macOS menu bar
python3 gui_app.py  # Linux GUI
```

### Organization Examples
```bash
# Before
Downloads/
├── photo.jpg
├── document.pdf
├── song.mp3
└── archive.zip

# After (Type + Size + Date)
Downloads/
├── images/small/10-2025/photo.jpg
├── documents/medium/10-2025/document.pdf
├── audio/small/10-2025/song.mp3
└── archives/small/10-2025/archive.zip
```

---

## 🛠️ Development & Building

### Universal Development
```bash
git clone https://github.com/AmirMGhanem/autoshelf.git
cd autoshelf

# Install all dependencies
pip install -r requirements-cross-platform.txt

# Test on current platform
python3 autoshelf.py
```

### Building for macOS
```bash
# Build standalone app
./build_app.sh
# Creates: dist/AutoShelf.app and AutoShelf-Installer.dmg
```

### Building for Linux
```bash
# Create distributable package
tar -czf autoshelf-linux.tar.gz *.py *.txt *.md *.png launcher_linux.sh

# Or create AppImage (advanced)
# Follow AppImage documentation
```

---

## 🐛 Troubleshooting

### macOS Issues
```bash
# Missing dependencies
pip install rumps pync pyobjc-framework-Cocoa

# Permission issues
# Go to System Preferences → Security & Privacy → Privacy
# Add Python to "Files and Folders" permissions
```

### Linux Issues
```bash
# Missing tkinter
sudo apt install python3-tk        # Ubuntu/Debian
sudo dnf install python3-tkinter   # Fedora
sudo pacman -S tk                   # Arch Linux

# Missing notifications
sudo apt install libnotify-bin      # Ubuntu/Debian

# Display issues (headless server)
export DISPLAY=:0                   # If using SSH with X forwarding
```

### General Issues
```bash
# Check platform detection
python3 -c "from platform_utils import *; log_platform_info()"

# Test file monitoring
python3 -c "from watchdog.observers import Observer; print('Watchdog OK')"

# Check permissions
ls -la ~/Downloads  # Make sure directory is readable/writable
```

---

## 🎯 Roadmap

### Planned Features
- [ ] **Windows support** (PyQt interface)
- [ ] **Advanced filtering rules** (custom extensions, size ranges)
- [ ] **Undo functionality** (restore organized files)
- [ ] **Scheduled organization** (run at specific times)
- [ ] **Cloud folder support** (Dropbox, Google Drive, etc.)
- [ ] **Multiple folder monitoring**
- [ ] **File tagging system**

### Platform-Specific Improvements
- [ ] **macOS**: Touch Bar support, Shortcuts app integration
- [ ] **Linux**: System service integration, KDE/GNOME extensions
- [ ] **Cross-platform**: Settings sync, unified config format

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Platform-specific help needed:**
- 🍎 **macOS developers**: Menu bar UX improvements
- 🐧 **Linux developers**: DE-specific integrations  
- 🪟 **Windows developers**: Native Windows interface

**Ideas? Bugs?** 
- Open an [issue](https://github.com/amirmghanem/autoshelf/issues)
- Include your OS and version
- Attach logs from "Show Logs" menu

---

## 📄 License

MIT License - Free to use, modify, and share

## 👨‍💻 Author

**Amir** - [@amirmghanem](https://github.com/amirmghanem)

---

<p align="center">
Made with ❤️ for productivity across all platforms
</p>