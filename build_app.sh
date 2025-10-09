#!/bin/bash

# Build script for AutoShelf
# Creates macOS app bundle and DMG installer

set -e

echo "=================================="
echo "Building AutoShelf.app"
echo "=================================="

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build app with py2app
echo "Building app bundle..."
./venv/bin/python setup.py py2app

# Check if build succeeded
if [ ! -d "dist/AutoShelf.app" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ App bundle created: dist/AutoShelf.app"

# Create DMG if create-dmg is available
if command -v create-dmg &> /dev/null; then
    echo ""
    echo "=================================="
    echo "Creating DMG installer"
    echo "=================================="
    
    # Remove old DMG if exists
    rm -f "AutoShelf-Installer.dmg"
    
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
    
    echo "✅ DMG created: AutoShelf-Installer.dmg"
else
    echo ""
    echo "⚠️  create-dmg not found"
    echo "Install with: brew install create-dmg"
    echo ""
    echo "You can still use the app from: dist/AutoShelf.app"
fi

echo ""
echo "=================================="
echo "Build Complete!"
echo "=================================="
echo ""
echo "App location: dist/AutoShelf.app"
echo "To install: Drag AutoShelf.app to Applications folder"
echo ""

