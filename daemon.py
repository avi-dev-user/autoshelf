#!/usr/bin/env python3
"""
AutoShelf Daemon Mode
Runs AutoShelf as a background service without GUI
"""
import sys
import os
import signal
import time
import atexit
import logging
from pathlib import Path
from datetime import datetime
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from auto_organizer import get_organizer
from platform_utils import get_platform, is_linux, log_platform_info
from version import __version__


class AutoShelfDaemon:
    """AutoShelf daemon for background operation"""
    
    def __init__(self, pidfile_path="/tmp/autoshelf.pid", log_path=None):
        self.pidfile_path = pidfile_path
        self.config = get_config()
        self.organizer = get_organizer()
        self.running = False
        
        # Setup logging
        if log_path is None:
            log_path = Path.home() / ".autoshelf" / "daemon.log"
            
        log_path.parent.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def daemonize(self):
        """Fork process to run as daemon"""
        try:
            # First fork
            pid = os.fork()
            if pid > 0:
                # Parent process exits
                sys.exit(0)
        except OSError as e:
            self.logger.error(f"Fork #1 failed: {e}")
            sys.exit(1)
        
        # Decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        
        try:
            # Second fork
            pid = os.fork()
            if pid > 0:
                # Second parent exits
                sys.exit(0)
        except OSError as e:
            self.logger.error(f"Fork #2 failed: {e}")
            sys.exit(1)
        
        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        
        # Write pidfile
        self.write_pidfile()
        
        # Register cleanup function
        atexit.register(self.cleanup)
        
        self.logger.info(f"AutoShelf daemon started with PID {os.getpid()}")
    
    def write_pidfile(self):
        """Write process ID to pidfile"""
        try:
            with open(self.pidfile_path, 'w') as f:
                f.write(str(os.getpid()))
        except Exception as e:
            self.logger.error(f"Failed to write pidfile: {e}")
            sys.exit(1)
    
    def read_pidfile(self):
        """Read PID from pidfile"""
        try:
            with open(self.pidfile_path, 'r') as f:
                pid = int(f.read().strip())
            return pid
        except (FileNotFoundError, ValueError):
            return None
    
    def remove_pidfile(self):
        """Remove pidfile"""
        try:
            if os.path.exists(self.pidfile_path):
                os.remove(self.pidfile_path)
        except Exception as e:
            self.logger.error(f"Failed to remove pidfile: {e}")
    
    def is_running(self):
        """Check if daemon is already running"""
        pid = self.read_pidfile()
        if pid is None:
            return False
            
        try:
            # Check if process exists
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            # Process doesn't exist, remove stale pidfile
            self.remove_pidfile()
            return False
        except PermissionError:
            # Process exists but we can't signal it
            return True
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        if self.running:
            self.logger.info(f"Received signal {signum}, shutting down...")
            self.stop()
            sys.exit(0)
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def start(self, foreground=False):
        """Start the daemon"""
        if self.is_running():
            self.logger.error("AutoShelf daemon is already running")
            return False
        
        self.logger.info(f"Starting AutoShelf daemon v{__version__}")
        log_platform_info()
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Fork to background unless running in foreground
        if not foreground:
            self.daemonize()
        else:
            self.write_pidfile()
            atexit.register(self.cleanup)
        
        # Main daemon loop
        self.running = True
        self.run()
        
        return True
    
    def stop(self):
        """Stop the daemon"""
        if not self.running:
            return
            
        try:
            self.running = False
            self.logger.info("AutoShelf daemon stopped")
            if hasattr(self, 'observer') and self.observer.is_alive():
                self.observer.stop()
                self.observer.join()
        except Exception as e:
            self.logger.error(f"Error stopping daemon: {e}")
        finally:
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
    
    def status(self):
        """Check daemon status"""
        if self.is_running():
            pid = self.read_pidfile()
            self.logger.info(f"AutoShelf daemon is running (PID {pid})")
            
            # Show additional status info
            watch_path = self.config.get_watch_path()
            methods = []
            if self.config.is_organize_by_type():
                methods.append("Type")
            if self.config.is_organize_by_size():
                methods.append("Size")  
            if self.config.is_organize_by_date():
                methods.append("Date")
            
            self.logger.info(f"Watching: {watch_path}")
            self.logger.info(f"Methods: {', '.join(methods) if methods else 'None'}")
            return True
        else:
            self.logger.info("AutoShelf daemon is not running")
            return False
    
    def restart(self):
        """Restart the daemon"""
        self.logger.info("Restarting AutoShelf daemon...")
        self.stop()
        time.sleep(2)
        return self.start()
    
    def run(self):
        """Main daemon loop"""
        try:
            # Start file monitoring
            if not self.organizer.start():
                self.logger.error("Failed to start file organizer")
                return
            
            self.logger.info("AutoShelf daemon is now monitoring files")
            
            # Health check variables
            last_health_check = time.time()
            health_check_interval = 60  # Check every minute
            
            # Main loop
            while self.running:
                try:
                    time.sleep(1)
                    
                    # Periodic health check
                    current_time = time.time()
                    if current_time - last_health_check >= health_check_interval:
                        self.health_check()
                        last_health_check = current_time
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.logger.error(f"Error in daemon loop: {e}")
                    time.sleep(5)  # Brief pause before continuing
            
        except Exception as e:
            self.logger.error(f"Fatal error in daemon: {e}")
        finally:
            self.cleanup()
    
    def health_check(self):
        """Perform health check"""
        try:
            # Check if organizer is still running
            if not self.organizer.is_running():
                self.logger.warning("File organizer stopped, restarting...")
                self.organizer.start()
            
            # Check if watch path still exists
            watch_path = Path(self.config.get_watch_path())
            if not watch_path.exists():
                self.logger.warning(f"Watch path {watch_path} no longer exists")
            
            # Log periodic status
            self.logger.debug("Health check passed")
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            if hasattr(self, 'organizer') and self.organizer.is_running():
                self.organizer.stop()
                self.logger.info("File organizer stopped")
            
            self.remove_pidfile()
            self.logger.info("AutoShelf daemon shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AutoShelf Daemon")
    parser.add_argument('command', choices=['start', 'stop', 'restart', 'status', 'foreground'], 
                       help='Daemon command')
    parser.add_argument('--pidfile', default='/tmp/autoshelf.pid',
                       help='PID file path')
    parser.add_argument('--logfile', 
                       help='Log file path (default: ~/.autoshelf/daemon.log)')
    
    args = parser.parse_args()
    
    # Create daemon instance
    daemon = AutoShelfDaemon(pidfile_path=args.pidfile, log_path=args.logfile)
    
    # Execute command
    if args.command == 'start':
        if daemon.start():
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.command == 'stop':
        if daemon.stop():
            sys.exit(0) 
        else:
            sys.exit(1)
    elif args.command == 'restart':
        if daemon.restart():
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.command == 'status':
        if daemon.status():
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.command == 'foreground':
        # Run in foreground (useful for debugging)
        try:
            daemon.start(foreground=True)
        except KeyboardInterrupt:
            daemon.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()