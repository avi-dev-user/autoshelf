import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".autoshelf"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        
        self.data = {
            "watch_path": str(Path.home() / "Downloads"),
            "last_organize": None,
            "organize_by_type": True,
            "organize_by_size": False,
            "organize_by_date": False,
            "show_tutorial": True
        }
        self.load()
    
    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.data.update(json.load(f))
            except:
                pass
    
    def save(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except:
            pass
    
    def get_watch_path(self):
        return self.data.get("watch_path", str(Path.home() / "Downloads"))
    
    def set_watch_path(self, path):
        self.data["watch_path"] = path
        self.save()
    
    def get_last_organize(self):
        return self.data.get("last_organize")
    
    def set_last_organize(self, timestamp):
        self.data["last_organize"] = timestamp
        self.save()
    
    def is_organize_by_type(self):
        return self.data.get("organize_by_type", True)
    
    def is_organize_by_size(self):
        return self.data.get("organize_by_size", False)
    
    def is_organize_by_date(self):
        return self.data.get("organize_by_date", False)
    
    def set_organize_by_type(self, enabled):
        self.data["organize_by_type"] = enabled
        self.save()
    
    def set_organize_by_size(self, enabled):
        self.data["organize_by_size"] = enabled
        self.save()
    
    def set_organize_by_date(self, enabled):
        self.data["organize_by_date"] = enabled
        self.save()
    
    def should_show_tutorial(self):
        return self.data.get("show_tutorial", True)
    
    def set_tutorial_shown(self):
        self.data["show_tutorial"] = False
        self.save()

_config = None

def get_config():
    global _config
    if _config is None:
        _config = Config()
    return _config
