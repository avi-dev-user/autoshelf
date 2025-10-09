# Changelog

All notable changes to AutoShelf will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-09

### Initial Release 🎉

#### Added
- **Smart File Organization**
  - Organize by file type (10+ categories)
  - Organize by file size (small/medium/large)
  - Organize by date added (month-year format)
  - Support for nested folder organization

- **Native macOS Interface**
  - Menu bar app with clean interface
  - Settings window with checkboxes
  - Live log viewer with auto-refresh
  - Native folder picker dialog

- **Real-time Monitoring**
  - Auto-organize new files as they appear
  - "Organize Existing Files" for batch processing
  - Configurable watch folders (Downloads, Documents, Desktop, custom)

- **File Type Support**
  - Images: .jpg, .png, .gif, .webp, etc.
  - Videos: .mp4, .mov, .avi, etc.
  - Documents: .pdf, .doc, .docx, .txt
  - Spreadsheets: .xls, .xlsx, .csv
  - Presentations: .ppt, .pptx, .key
  - Archives: .zip, .rar, .tar, .gz
  - Software: .exe, .dmg, .pkg, .app
  - Code: .py, .js, .java, .html
  - Audio: .mp3, .wav, .aac
  - Others: everything else

- **Features**
  - Persistent settings (saved to ~/.autoshelf/config.json)
  - Duplicate file handling (auto-rename)
  - Live logging with timestamps and clean formatting
  - macOS notifications when files are organized (with sound)
  - Interactive tutorial on first launch
  - "How to Use" menu item to replay tutorial
  - About dialog with project info
  - MIT License (Open Source)

#### Technical Details
- Built with Python 3.9+
- Uses rumps for menu bar interface
- Uses watchdog for file monitoring
- Uses PyObjC for native macOS UI
- Minimal dependencies (3 packages)
- No external APIs required
- No internet connection needed

---

## Future Versions

### Planned for v1.1.0
- [ ] Custom organization rules
- [ ] File preview in settings
- [ ] Undo last organization
- [ ] Statistics dashboard

### Ideas for v2.0.0
- [ ] Cloud sync support
- [ ] Multi-folder monitoring
- [ ] Advanced filtering
- [ ] Scheduled organization

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to this changelog and the project.

