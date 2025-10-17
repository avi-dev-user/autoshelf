#!/usr/bin/env python3
"""
AutoShelf Health Monitor
Monitors AutoShelf daemon and restarts if needed
"""
import sys
import time
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from platform_utils import send_notification


class HealthMonitor:
    """Health monitoring for AutoShelf daemon"""
    
    def __init__(self):
        self.config = get_config()
        self.health_file = Path.home() / ".autoshelf" / "health.json"
        self.log_file = Path.home() / ".autoshelf" / "health.log"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Health check configuration
        self.check_interval = 30  # seconds
        self.max_failures = 3
        self.restart_cooldown = 300  # 5 minutes
        
    def load_health_data(self):
        """Load health tracking data"""
        try:
            if self.health_file.exists():
                with open(self.health_file) as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load health data: {e}")
        
        return {
            'last_check': None,
            'failure_count': 0,
            'last_restart': None,
            'total_restarts': 0,
            'uptime_start': None
        }
    
    def save_health_data(self, data):
        """Save health tracking data"""
        try:
            self.health_file.parent.mkdir(exist_ok=True)
            with open(self.health_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save health data: {e}")
    
    def is_daemon_running(self):
        """Check if AutoShelf daemon is running"""
        try:
            pidfile = Path.home() / ".autoshelf" / "autoshelf.pid"
            if not pidfile.exists():
                return False
            
            with open(pidfile) as f:
                pid = int(f.read().strip())
            
            # Check if process exists and is our daemon
            try:
                with open(f"/proc/{pid}/cmdline") as f:
                    cmdline = f.read()
                return "daemon.py" in cmdline or "autoshelf" in cmdline
            except (FileNotFoundError, PermissionError):
                return False
                
        except Exception:
            return False
    
    def is_daemon_responsive(self):
        """Check if daemon is responsive (processing files)"""
        try:
            # Check if watch directory is being monitored
            watch_path = Path(self.config.get_watch_path())
            if not watch_path.exists():
                return False
            
            # Check recent activity by looking at log timestamps
            daemon_log = Path.home() / ".autoshelf" / "daemon.log"
            if daemon_log.exists():
                # Check if there's been recent activity (within last 5 minutes)
                mtime = datetime.fromtimestamp(daemon_log.stat().st_mtime)
                if datetime.now() - mtime < timedelta(minutes=5):
                    return True
            
            return True  # Assume responsive if no recent errors
            
        except Exception as e:
            self.logger.warning(f"Failed to check daemon responsiveness: {e}")
            return False
    
    def start_daemon(self):
        """Start the AutoShelf daemon"""
        try:
            daemon_script = Path(__file__).parent / "daemon.py"
            subprocess.run([sys.executable, str(daemon_script), "start"], 
                          check=True, capture_output=True)
            self.logger.info("AutoShelf daemon started")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to start daemon: {e}")
            return False
    
    def restart_daemon(self):
        """Restart the AutoShelf daemon"""
        try:
            daemon_script = Path(__file__).parent / "daemon.py"
            subprocess.run([sys.executable, str(daemon_script), "restart"], 
                          check=True, capture_output=True)
            self.logger.info("AutoShelf daemon restarted")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to restart daemon: {e}")
            return False
    
    def perform_health_check(self):
        """Perform comprehensive health check"""
        health_data = self.load_health_data()
        now = datetime.now().isoformat()
        
        self.logger.debug("Performing health check...")
        
        # Check if daemon is running
        is_running = self.is_daemon_running()
        is_responsive = self.is_daemon_responsive() if is_running else False
        
        # Update health data
        health_data['last_check'] = now
        
        if is_running and is_responsive:
            # Daemon is healthy
            health_data['failure_count'] = 0
            if health_data['uptime_start'] is None:
                health_data['uptime_start'] = now
            
            self.logger.debug("Health check: PASS")
            
        else:
            # Daemon is not healthy
            health_data['failure_count'] += 1
            health_data['uptime_start'] = None
            
            self.logger.warning(f"Health check: FAIL (running={is_running}, responsive={is_responsive})")
            
            # Check if we should restart
            if health_data['failure_count'] >= self.max_failures:
                last_restart = health_data.get('last_restart')
                if last_restart:
                    last_restart_time = datetime.fromisoformat(last_restart)
                    if datetime.now() - last_restart_time < timedelta(seconds=self.restart_cooldown):
                        self.logger.info(f"Restart cooldown active, waiting...")
                        self.save_health_data(health_data)
                        return
                
                # Attempt restart
                self.logger.info("Attempting to restart daemon due to health failures")
                if self.restart_daemon():
                    health_data['failure_count'] = 0
                    health_data['last_restart'] = now
                    health_data['total_restarts'] += 1
                    health_data['uptime_start'] = now
                    
                    # Send notification
                    send_notification(
                        "AutoShelf Health Monitor",
                        "Daemon restarted due to health check failure"
                    )
                else:
                    self.logger.error("Failed to restart daemon")
        
        self.save_health_data(health_data)
    
    def get_health_status(self):
        """Get current health status"""
        health_data = self.load_health_data()
        
        status = {
            'running': self.is_daemon_running(),
            'responsive': self.is_daemon_responsive(),
            'failure_count': health_data.get('failure_count', 0),
            'total_restarts': health_data.get('total_restarts', 0),
            'last_check': health_data.get('last_check'),
            'last_restart': health_data.get('last_restart'),
            'uptime_start': health_data.get('uptime_start')
        }
        
        if status['uptime_start']:
            uptime_start = datetime.fromisoformat(status['uptime_start'])
            uptime = datetime.now() - uptime_start
            status['uptime_seconds'] = uptime.total_seconds()
        else:
            status['uptime_seconds'] = 0
        
        return status
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.logger.info("Starting AutoShelf health monitor")
        
        try:
            while True:
                self.perform_health_check()
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Health monitor stopped by user")
        except Exception as e:
            self.logger.error(f"Health monitor error: {e}")
    
    def show_status(self):
        """Show current status"""
        status = self.get_health_status()
        
        print("AutoShelf Health Status")
        print("=" * 30)
        print(f"Daemon Running:    {'✅ Yes' if status['running'] else '❌ No'}")
        print(f"Responsive:        {'✅ Yes' if status['responsive'] else '❌ No'}")
        print(f"Failure Count:     {status['failure_count']}")
        print(f"Total Restarts:    {status['total_restarts']}")
        
        if status['uptime_seconds'] > 0:
            uptime = timedelta(seconds=int(status['uptime_seconds']))
            print(f"Current Uptime:    {uptime}")
        else:
            print(f"Current Uptime:    Not running")
        
        if status['last_check']:
            print(f"Last Check:        {status['last_check']}")
        
        if status['last_restart']:
            print(f"Last Restart:      {status['last_restart']}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AutoShelf Health Monitor")
    parser.add_argument('command', choices=['monitor', 'status', 'check'], 
                       help='Monitor command')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor()
    
    if args.command == 'monitor':
        monitor.monitor_loop()
    elif args.command == 'status':
        monitor.show_status()
    elif args.command == 'check':
        monitor.perform_health_check()
        monitor.show_status()


if __name__ == "__main__":
    main()