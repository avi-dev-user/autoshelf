"""
Cross-platform utilities for AutoShelf
Detects operating system and provides appropriate interfaces
"""
import platform
import sys


def get_platform():
    """Get the current platform name"""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    elif system == 'linux':
        return 'linux'
    elif system == 'windows':
        return 'windows'
    else:
        return 'unknown'


def is_macos():
    """Check if running on macOS"""
    return get_platform() == 'macos'


def is_linux():
    """Check if running on Linux"""
    return get_platform() == 'linux'


def is_windows():
    """Check if running on Windows"""
    return get_platform() == 'windows'


def can_use_system_tray():
    """Check if system tray is available"""
    if is_macos():
        try:
            import rumps
            return True
        except ImportError:
            return False
    elif is_linux():
        # Check for system tray support
        try:
            import os
            return 'DISPLAY' in os.environ
        except:
            return False
    return False


def get_default_downloads_folder():
    """Get the default downloads folder for the current platform"""
    from pathlib import Path
    
    if is_macos() or is_linux():
        return str(Path.home() / "Downloads")
    elif is_windows():
        return str(Path.home() / "Downloads")
    else:
        return str(Path.home())


def send_notification(title, message, app_name="AutoShelf"):
    """Send a cross-platform notification"""
    from pathlib import Path
    
    if is_macos():
        try:
            import pync
            pync.notify(
                message,
                title=title,
                appIcon=str(Path(__file__).parent / "logo.png"),
                sound="Glass"
            )
            return True
        except ImportError:
            pass
    
    elif is_linux():
        try:
            import subprocess
            # Try notify-send (most common)
            subprocess.run([
                'notify-send', 
                f'{app_name}: {title}', 
                message,
                '--icon=dialog-information'
            ], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Try zenity as fallback
                subprocess.run([
                    'zenity', '--info',
                    '--title', f'{app_name}: {title}',
                    '--text', message,
                    '--width', '300'
                ], check=True, capture_output=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
    
    # Fallback: print to console
    print(f"[{app_name}] {title}: {message}")
    return False


def log_platform_info():
    """Log information about the current platform"""
    print(f"Platform: {get_platform()}")
    print(f"Python: {sys.version}")
    print(f"System tray available: {can_use_system_tray()}")
    print(f"Default downloads: {get_default_downloads_folder()}")