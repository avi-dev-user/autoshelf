# Building AutoShelf

Instructions for building AutoShelf into a standalone macOS application.

## Prerequisites

1. **Python 3.9+** installed
2. **py2app** installed: `pip install py2app`
3. **create-dmg** (optional): `brew install create-dmg`

## Quick Build

```bash
# Make sure you're in the project directory
cd autoshelf

# Run the build script
./build_app.sh
```

This will create:
- `dist/AutoShelf.app` - The standalone application
- `AutoShelf-Installer.dmg` - DMG installer (if create-dmg is installed)

## Manual Build Steps

### Step 1: Build the App Bundle

```bash
# Activate virtual environment
source venv/bin/activate

# Clean previous builds
rm -rf build dist

# Build with py2app
python setup.py py2app
```

This creates `dist/AutoShelf.app`

### Step 2: Test the App

```bash
# Run the built app
open dist/AutoShelf.app
```

The app should appear in your menu bar.

### Step 3: Create DMG Installer (Optional)

```bash
# Install create-dmg if needed
brew install create-dmg

# Create DMG
create-dmg \
    --volname "AutoShelf Installer" \
    --volicon "logo.png" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "AutoShelf.app" 175 120 \
    --hide-extension "AutoShelf.app" \
    --app-drop-link 425 120 \
    "AutoShelf-Installer.dmg" \
    "dist/"
```

This creates `AutoShelf-Installer.dmg`

## Distribution

### For Users:
1. Download `AutoShelf-Installer.dmg`
2. Open the DMG
3. Drag AutoShelf.app to Applications folder
4. Run from Applications or Spotlight

### For Developers:
The app bundle in `dist/AutoShelf.app` contains:
- All Python code
- All dependencies
- App icon
- Resources

No Python installation required for end users!

## Troubleshooting

### "Build failed"
- Make sure py2app is installed: `pip install py2app`
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Try: `python setup.py py2app -A` (alias mode for testing)

### "App won't open"
- Right-click → Open (to bypass Gatekeeper on first run)
- Check Console.app for error messages
- Try running from Terminal: `./dist/AutoShelf.app/Contents/MacOS/AutoShelf`

### "Missing dependencies"
Make sure requirements.txt includes all packages used in the code.

### "Icon not showing"
- Ensure `logo.png` exists
- Make sure it's referenced in `setup.py` under `iconfile`
- Rebuild the app

## Build Configuration

The build is configured in `setup.py`:
- **iconfile**: App icon (logo.png)
- **LSUIElement**: True (menu bar app, no dock icon)
- **packages**: All required Python packages
- **includes**: Project modules

## Size Optimization

To reduce app size:
1. Remove unnecessary packages from requirements.txt
2. Use `--optimize 2` in setup.py OPTIONS
3. Strip debug symbols: `strip dist/AutoShelf.app/Contents/MacOS/AutoShelf`

## Code Signing (Optional)

For distribution outside the Mac App Store:

```bash
# Sign the app
codesign --deep --force --sign "Developer ID Application: Your Name" dist/AutoShelf.app

# Create signed DMG
codesign --sign "Developer ID Application: Your Name" AutoShelf-Installer.dmg

# Notarize with Apple (requires developer account)
xcrun altool --notarize-app --file AutoShelf-Installer.dmg ...
```

## Quick Reference

```bash
# Build everything
./build_app.sh

# Build app only (no DMG)
python setup.py py2app

# Build for testing (faster, not standalone)
python setup.py py2app -A

# Clean builds
rm -rf build dist *.dmg
```

---

Built with py2app and love ❤️

