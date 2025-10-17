#!/usr/bin/env python3
"""
AutoShelf - Cross-platform File Organizer
Automatically detects platform and launches appropriate interface
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from platform_utils import get_platform, is_macos, is_linux, log_platform_info
from version import __version__


def show_platform_error():
    """Show error for unsupported platforms"""
    platform = get_platform()
    print(f"❌ AutoShelf v{__version__}")
    print(f"Platform '{platform}' is not supported yet.")
    print("\nSupported platforms:")
    print("  • macOS (Darwin) - Menu bar interface")
    print("  • Linux - GUI interface")
    print("\nWindows support coming soon!")
    sys.exit(1)


def check_dependencies():
    """Check if required dependencies are available"""
    missing = []
    
    if is_macos():
        try:
            import rumps
            import pync
        except ImportError as e:
            missing.append(f"macOS: {e.name}")
    
    elif is_linux():
        try:
            import tkinter
        except ImportError:
            missing.append("Linux: tkinter (usually python3-tk package)")
    
    # Common dependencies
    try:
        import watchdog
    except ImportError:
        missing.append("watchdog")
    
    if missing:
        print(f"❌ Missing dependencies:")
        for dep in missing:
            print(f"   • {dep}")
        print(f"\nInstall with: pip install -r requirements.txt")
        if is_linux():
            print("For Linux, you may also need: sudo apt install python3-tk")
        sys.exit(1)


def launch_macos():
    """Launch macOS version with menu bar interface"""
    print("🍎 Starting AutoShelf for macOS...")
    try:
        from main import AutoShelf
        app = AutoShelf()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start macOS version: {e}")
        sys.exit(1)


def launch_linux():
    """Launch Linux version with GUI interface"""
    print("🐧 Starting AutoShelf for Linux...")
    try:
        from gui_app import AutoShelfGUI
        app = AutoShelfGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start Linux version: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have a display server running (X11/Wayland)")
        print("2. Install tkinter: sudo apt install python3-tk")
        print("3. Install dependencies: pip install -r requirements.txt")
        sys.exit(1)


def launch_daemon():
    """Launch daemon mode"""
    print("🔧 Starting AutoShelf in daemon mode...")
    try:
        from daemon import AutoShelfDaemon
        daemon = AutoShelfDaemon()
        daemon.start(foreground=True)
    except Exception as e:
        print(f"❌ Failed to start daemon: {e}")
        sys.exit(1)


def main():
    """Main entry point - detects platform and launches appropriate interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AutoShelf - Cross-platform File Organizer")
    parser.add_argument('--daemon', action='store_true', help='Run as background daemon')
    parser.add_argument('--service', choices=['install', 'uninstall', 'start', 'stop', 'status'], 
                       help='Service management commands')
    
    args = parser.parse_args()
    
    print(f"📂 AutoShelf v{__version__} - Cross-platform File Organizer")
    print("=" * 50)
    
    # Handle service commands
    if args.service:
        handle_service_command(args.service)
        return
    
    # Handle daemon mode
    if args.daemon:
        launch_daemon()
        return
    
    # Show platform information
    log_platform_info()
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Launch platform-specific interface
    if is_macos():
        launch_macos()
    elif is_linux():
        launch_linux()
    else:
        show_platform_error()


def handle_service_command(command):
    """Handle systemd service commands"""
    if not is_linux():
        print("❌ Service management is only available on Linux")
        sys.exit(1)
    
    try:
        if command == 'install':
            install_service()
        elif command == 'uninstall':
            uninstall_service()
        elif command == 'start':
            start_service()
        elif command == 'stop':
            stop_service()
        elif command == 'status':
            service_status()
    except Exception as e:
        print(f"❌ Service command failed: {e}")
        sys.exit(1)


def install_service():
    """Install systemd service"""
    import subprocess
    import shutil
    
    username = os.environ.get('USER')
    if not username:
        print("❌ Could not determine username")
        sys.exit(1)
    
    # Copy service file
    service_file = Path(__file__).parent / "autoshelf@.service"
    target_dir = Path.home() / ".config/systemd/user"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    target_file = target_dir / "autoshelf@.service"
    shutil.copy2(service_file, target_file)
    
    print(f"✅ Service file copied to {target_file}")
    
    # Reload systemd and enable service
    try:
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
        subprocess.run(['systemctl', '--user', 'enable', f'autoshelf@{username}.service'], check=True)
        print(f"✅ Service autoshelf@{username} installed and enabled")
        print("\n📋 Service commands:")
        print(f"  Start:   systemctl --user start autoshelf@{username}")
        print(f"  Stop:    systemctl --user stop autoshelf@{username}")
        print(f"  Status:  systemctl --user status autoshelf@{username}")
        print(f"  Logs:    journalctl --user -f -u autoshelf@{username}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup service: {e}")
        sys.exit(1)


def uninstall_service():
    """Uninstall systemd service"""
    import subprocess
    
    username = os.environ.get('USER')
    service_name = f'autoshelf@{username}.service'
    
    try:
        # Stop and disable service
        subprocess.run(['systemctl', '--user', 'stop', service_name], check=False)
        subprocess.run(['systemctl', '--user', 'disable', service_name], check=False)
        
        # Remove service file
        target_file = Path.home() / ".config/systemd/user/autoshelf@.service"
        if target_file.exists():
            target_file.unlink()
        
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
        print(f"✅ Service {service_name} uninstalled")
        
    except Exception as e:
        print(f"❌ Failed to uninstall service: {e}")


def start_service():
    """Start systemd service"""
    import subprocess
    
    username = os.environ.get('USER')
    service_name = f'autoshelf@{username}.service'
    
    try:
        subprocess.run(['systemctl', '--user', 'start', service_name], check=True)
        print(f"✅ Service {service_name} started")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to start service {service_name}")


def stop_service():
    """Stop systemd service"""
    import subprocess
    
    username = os.environ.get('USER')
    service_name = f'autoshelf@{username}.service'
    
    try:
        subprocess.run(['systemctl', '--user', 'stop', service_name], check=True)
        print(f"✅ Service {service_name} stopped")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to stop service {service_name}")


def service_status():
    """Check systemd service status"""
    import subprocess
    
    username = os.environ.get('USER')
    service_name = f'autoshelf@{username}.service'
    
    try:
        result = subprocess.run(['systemctl', '--user', 'is-active', service_name], 
                              capture_output=True, text=True)
        status = result.stdout.strip()
        
        if status == 'active':
            print(f"✅ Service {service_name} is running")
        else:
            print(f"⏸️ Service {service_name} is {status}")
        
        # Show detailed status
        subprocess.run(['systemctl', '--user', 'status', service_name, '--no-pager'])
        
    except subprocess.CalledProcessError:
        print(f"❌ Service {service_name} not found or error occurred")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 AutoShelf stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)