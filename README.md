# AutoShelf 📂

> Smart file organization for macOS. No AI. No setup. Just works.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![macOS](https://img.shields.io/badge/macOS-11.0+-blue.svg)](https://www.apple.com/macos/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Automatically organize your Downloads folder by file type, size, and date. Lives in your menu bar, works in the background.

## Quick Start

### For Users (Standalone App)

1. **[Download AutoShelf-Installer.dmg](https://github.com/AmirMGhanem/autoshelf/releases/download/v0.1/AutoShelf-Installer.dmg)**
2. Open the DMG file
3. Drag **AutoShelf.app** to your **Applications** folder
4. Launch AutoShelf from Applications or Spotlight
5. Follow the welcome tutorial

**Run on Startup (Optional):**
1. Open **System Settings** (or **System Preferences** on older macOS)
2. Go to **General** → **Login Items** (or **Users & Groups** → **Login Items**)
3. Click the **+** button and select **AutoShelf.app** from Applications
4. AutoShelf will now start automatically when you log in

### For Developers (From Source)

```bash
# Install dependencies
pip install -r requirements.txt

# Run from source
python main.py
```

Then:
1. Click **Settings** → Choose organization methods
2. Click **Auto-Organize New Files** → Start watching
3. Done! New files are organized automatically

## Organization Methods

**By File Type** (10 categories)
- images, videos, documents, spreadsheets, presentations
- archives, software, code, audio, others

**By File Size**
- small (< 1MB), medium (1-50MB), large (> 50MB)

**By Date Added**
- Folders by month-year (10-2025, 09-2025...)

**Combine Methods** for nested folders:
```
images/small/10-2025/photo.jpg
documents/medium/09-2025/report.pdf
```

## Features

- Real-time file monitoring
- macOS native notifications
- Live log viewer
- Works offline (no API keys)
- Clean, simple interface

## Menu

- **Settings** - Choose organization methods
- **Auto-Organize New Files** - Start/stop watching
- **Organize Existing Files** - Batch organize current files
- **Watch Folder** - Change monitored folder
- **Show Logs** - See what's happening
- **How to Use** - Replay tutorial
- **About** - App info

## Examples

```bash
# Type only
photo.jpg → images/
document.pdf → documents/

# Type + Size
photo.jpg (500KB) → images/small/
video.mp4 (100MB) → videos/large/

# All three
photo.jpg (500KB, Oct 2025) → images/small/10-2025/
```

## Building Standalone App

Want to build the .app yourself?

```bash
# Build app bundle and DMG
./build_app.sh

# Output:
# - dist/AutoShelf.app (standalone app)
# - AutoShelf-Installer.dmg (installer)
```

See [BUILD.md](BUILD.md) for detailed build instructions.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ideas?** Open an [issue](https://github.com/amirmghanem/autoshelf/issues)

**Found a bug?** Please report it with logs from "Show Logs" menu

## License

MIT License - Free to use, modify, and share

## Author

**Amir** - [@amirmghanem](https://github.com/amirmghanem)

---

Made with ❤️ for productivity
# autoshelf
