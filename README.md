# AutoShelf 📂

> Smart file organization for macOS. No AI. No setup. Just works.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![macOS](https://img.shields.io/badge/macOS-11.0+-blue.svg)](https://www.apple.com/macos/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Automatically organize your Downloads folder by file type, size, and date. Lives in your menu bar, works in the background.

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
python main.py
```

Follow the welcome tutorial, or:
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
