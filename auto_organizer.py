"""
File organization engine
Watches directories and organizes files by type, size, and date
"""
import shutil
import time
import mimetypes
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import get_config

try:
    import pync
    HAS_PYNC = True
except ImportError:
    HAS_PYNC = False


def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


class FileOrganizer(FileSystemEventHandler):
    """Handles file system events and organizes files"""
    
    def __init__(self, watch_path):
        super().__init__()
        self.watch_path = Path(watch_path)
        self.config = get_config()
    
    def on_created(self, event):
        """Called when a new file is created"""
        if not event.is_directory:
            log("")
            log("-" * 60)
            log(f"NEW FILE: {Path(event.src_path).name}")
            time.sleep(0.5)
            self.organize(event.src_path)
            log("-" * 60)
    
    def organize(self, file_path):
        """Organize a single file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists() or file_path.parent != self.watch_path:
                return
            
            # Build folder hierarchy based on enabled methods
            folders = []
            if self.config.is_organize_by_type():
                folders.append(self._get_type_folder(file_path))
            if self.config.is_organize_by_size():
                folders.append(self._get_size_folder(file_path))
            if self.config.is_organize_by_date():
                folders.append(self._get_date_folder(file_path))
            
            if not folders:
                folders = ["unsorted"]
            
            # Create destination
            target = self.watch_path
            for folder in folders:
                target = target / folder
            target.mkdir(parents=True, exist_ok=True)
            
            # Handle duplicates
            dest = target / file_path.name
            counter = 1
            while dest.exists():
                dest = target / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
            
            # Move file
            shutil.move(str(file_path), str(dest))
            dest_path = '/'.join(folders)
            log(f"   Moved to: {dest_path}/")
            log(f"   Done")
            
            # Notify
            if HAS_PYNC:
                try:
                    pync.notify(
                        f"Moved to: {dest_path}/",
                        title=f"{file_path.name}",
                        appIcon=str(Path(__file__).parent / "logo.png"),
                        sound="Glass"
                    )
                except:
                    pass
        except Exception as e:
            log(f"   Error: {e}")
    
    def _get_type_folder(self, file_path):
        """Get folder name based on file type"""
        mime, _ = mimetypes.guess_type(str(file_path))
        ext = file_path.suffix.lower()
        
        if mime and mime.startswith('image'):
            return "images"
        if mime and mime.startswith('video'):
            return "videos"
        if ext in ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf']:
            return "documents"
        if ext in ['.xls', '.xlsx', '.csv']:
            return "spreadsheets"
        if ext in ['.ppt', '.pptx', '.key']:
            return "presentations"
        if ext in ['.zip', '.rar', '.tar', '.gz', '.7z', '.dmg']:
            return "archives"
        if ext in ['.exe', '.msi', '.app', '.pkg']:
            return "software"
        if ext in ['.py', '.js', '.java', '.cpp', '.html', '.css']:
            return "code"
        if mime and mime.startswith('audio'):
            return "audio"
        return "others"
    
    def _get_size_folder(self, file_path):
        """Get folder name based on file size"""
        size = file_path.stat().st_size
        if size < 1_000_000:
            return "small"
        elif size < 50_000_000:
            return "medium"
        return "large"
    
    def _get_date_folder(self, file_path):
        """Get folder name based on file creation date"""
        timestamp = file_path.stat().st_ctime
        date = datetime.fromtimestamp(timestamp)
        return date.strftime("%m-%Y")


class AutoOrganizer:
    """Main organizer that manages file watching"""
    
    def __init__(self):
        self.config = get_config()
        self.watch_path = self.config.get_watch_path()
        self.observer = None
    
    def start(self):
        """Start watching for new files"""
        log("")
        log("=" * 20)
        log("STARTED")
        log("-" * 20)
        log(f"Watching: {self.watch_path}")
        
        if self.observer and self.observer.is_alive():
            log("Already running")
            log("=" * 20)
            log("")
            return False
        
        # Ensure path exists
        Path(self.watch_path).mkdir(parents=True, exist_ok=True)
        
        # Show active methods
        methods = []
        if self.config.is_organize_by_type():
            methods.append("Type")
        if self.config.is_organize_by_size():
            methods.append("Size")
        if self.config.is_organize_by_date():
            methods.append("Date")
        
        log(f"Methods: {', '.join(methods) if methods else 'None'}")
        log("-" * 20)
        log("Waiting for files...")
        log("=" * 20)
        log("")
        
        self.observer = Observer()
        self.observer.schedule(FileOrganizer(self.watch_path), str(self.watch_path), recursive=False)
        self.observer.start()
        return True
    
    def stop(self):
        """Stop watching"""
        log("")
        log("=" * 20)
        log("STOPPED")
        log("=" * 20)
        log("")
        
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            return True
        return False
    
    def is_running(self):
        return self.observer and self.observer.is_alive()
    
    def set_watch_path(self, path):
        """Change watched directory"""
        was_running = self.is_running()
        if was_running:
            self.stop()
        self.watch_path = path
        self.config.set_watch_path(path)
        if was_running:
            self.start()
    
    def organize_existing_files(self):
        """Organize all files currently in the watch folder"""
        path = Path(self.watch_path)
        if not path.exists():
            return 0
        
        files = [f for f in path.iterdir() if f.is_file()]
        if not files:
            return 0
        
        log("")
        log("=" * 20)
        log(f"ORGANIZING {len(files)} FILE(S)")
        log("=" * 20)
        log("")
        
        organizer = FileOrganizer(self.watch_path)
        for i, file_path in enumerate(files, 1):
            log(f"[{i}/{len(files)}] {file_path.name}")
            organizer.organize(str(file_path))
            log("")
        
        log("=" * 20)
        log("COMPLETED")
        log("=" * 20)
        log("")
        return len(files)


_organizer = None

def get_organizer():
    global _organizer
    if _organizer is None:
        _organizer = AutoOrganizer()
    return _organizer
