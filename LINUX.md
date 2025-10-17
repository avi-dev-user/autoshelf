# AutoShelf Linux Edition 🐧

AutoShelf now works on Linux! This version provides a beautiful GUI interface using Python's tkinter.

## Quick Start (Linux)

### Installation

1. **Clone or download this repository**
2. **Install system dependencies:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-tk libnotify-bin

# Fedora/RHEL/CentOS
sudo dnf install python3 python3-pip python3-tkinter libnotify

# Arch Linux  
sudo pacman -S python python-pip tk libnotify

# OpenSUSE
sudo zypper install python3 python3-pip python3-tk libnotify-tools
```

3. **Run AutoShelf:**
```bash
./run_linux.sh
```

That's it! The script will automatically:
- Create a virtual environment
- Install Python dependencies
- Launch the GUI application

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements-linux.txt

# Run the application
python3 gui_app.py
```

## Linux GUI Features

### 🎨 Modern Interface
- Beautiful, modern GUI built with tkinter
- Responsive design with hover effects
- Intuitive layout and controls

### 📂 File Organization
- Same powerful organization as macOS version
- Organize by file type, size, and date
- Real-time monitoring with visual feedback

### 🔔 Desktop Notifications  
- Native Linux notifications via `notify-send`
- Shows file organization progress
- Status updates and alerts

### ⚙️ Easy Configuration
- Graphical settings window
- Toggle organization methods with checkboxes
- Choose watch folders with file browser

### 📊 Live Monitoring
- Real-time log viewer window
- See exactly what's happening
- Debug and track file movements

## GUI Screenshots

The Linux version includes:

- **Main Window**: Control panel with large, clear buttons
- **Settings Window**: Checkboxes to enable/disable organization methods  
- **Log Window**: Live scrolling log viewer
- **Folder Selection**: Quick buttons for common folders + custom chooser

## Cross-Platform Compatibility

| Feature | Linux | macOS | Windows |
|---------|--------|-------|---------|
| File Organization | ✅ | ✅ | 🟡* |
| GUI Interface | ✅ | ✅ | 🟡* |
| Desktop Notifications | ✅ | ✅ | 🟡* |
| System Tray | 🔄 | ✅ | 🔄 |
| Auto-start | 🔄 | ✅ | 🔄 |

*🟡 = Planned for future release  
🔄 = In development

## System Requirements

### Minimum
- Python 3.7+
- tkinter (usually included with Python)
- 50MB disk space

### Recommended  
- Python 3.9+
- libnotify (for desktop notifications)
- 100MB disk space

## Troubleshooting

### "tkinter not found"
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### "notify-send not found"
```bash
# Ubuntu/Debian  
sudo apt install libnotify-bin

# Fedora
sudo dnf install libnotify

# Arch
sudo pacman -S libnotify
```

### Permission errors
Make sure the script is executable:
```bash
chmod +x run_linux.sh
```

## Development

To contribute to Linux support:

1. Fork the repository
2. Create feature branch: `git checkout -b linux-feature`
3. Test on multiple distributions
4. Submit pull request

### Testing Distributions

We test on:
- Ubuntu 20.04+
- Fedora 35+  
- Arch Linux
- Debian 11+
- openSUSE Leap 15+

## Future Linux Features

- [ ] System tray integration
- [ ] Desktop file for application launcher
- [ ] Auto-start on login
- [ ] Flatpak/Snap packages
- [ ] Dark/Light theme support
- [ ] Keyboard shortcuts

## License

Same MIT license as the original AutoShelf project.

---

Made with ❤️ for Linux users who want organized files!