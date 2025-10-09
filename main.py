"""
AutoShelf - macOS File Organizer
Automatically organizes files by type, size, and date
"""
import rumps
import objc
import sys
from pathlib import Path
from datetime import datetime
from AppKit import (NSWindow, NSScrollView, NSButton, NSTextView, NSFont, 
                    NSOpenPanel, NSMakeRect, NSBackingStoreBuffered,
                    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, 
                    NSWindowStyleMaskResizable, NSButtonTypeSwitch)
from Foundation import NSObject, NSURL, NSTimer
from config import get_config
from auto_organizer import get_organizer
from version import __version__, __author__, __url__


class LogCapture:
    """Captures stdout for display in log window"""
    def __init__(self):
        self.logs = []
        self.max_logs = 1000
        self.original_stdout = sys.stdout
    
    def write(self, text):
        if text.strip():
            self.logs.append(text + '\n')
            if len(self.logs) > self.max_logs:
                self.logs.pop(0)
        self.original_stdout.write(text)
    
    def flush(self):
        self.original_stdout.flush()
    
    def get_logs(self):
        return ''.join(self.logs)


_log_capture = LogCapture()
sys.stdout = _log_capture


class LogWindow(NSObject):
    """Window displaying live application logs"""
    
    def initWithApp_(self, app):
        self = objc.super(LogWindow, self).init()
        if self is None:
            return None
        self.app = app
        self.window = None
        self.text_view = None
        return self
    
    def showWindow(self):
        if self.window:
            self.window.makeKeyAndOrderFront_(None)
            return
        
        # Create window
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 700, 500),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered, False
        )
        self.window.setTitle_("AutoShelf - Logs")
        self.window.setReleasedWhenClosed_(False)
        
        # Scrollable text view
        scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(0, 40, 700, 460))
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.setAutoresizingMask_(18)
        
        self.text_view = NSTextView.alloc().initWithFrame_(scroll_view.bounds())
        self.text_view.setEditable_(False)
        self.text_view.setFont_(NSFont.fontWithName_size_("Menlo", 11))
        scroll_view.setDocumentView_(self.text_view)
        
        # Clear button
        clear_btn = NSButton.alloc().initWithFrame_(NSMakeRect(20, 5, 100, 30))
        clear_btn.setTitle_("Clear")
        clear_btn.setBezelStyle_(1)
        clear_btn.setTarget_(self)
        clear_btn.setAction_("clearLogs:")
        
        self.window.contentView().addSubview_(scroll_view)
        self.window.contentView().addSubview_(clear_btn)
        self.window.makeKeyAndOrderFront_(None)
        
        # Auto-refresh timer
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.5, self, "updateLogs:", None, True
        )
    
    def updateLogs_(self, timer):
        if self.text_view:
            logs = _log_capture.get_logs()
            self.text_view.setString_(logs)
            self.text_view.scrollRangeToVisible_((len(logs), 0))
    
    def clearLogs_(self, sender):
        _log_capture.logs.clear()
        if self.text_view:
            self.text_view.setString_("")


class SettingsWindow(NSObject):
    """Settings window for choosing organization methods"""
    
    def initWithApp_(self, app):
        self = objc.super(SettingsWindow, self).init()
        if self is None:
            return None
        self.app = app
        self.window = None
        return self
    
    def showWindow(self):
        # Create window
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 400, 250),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered, False
        )
        self.window.setTitle_("Organization Settings")
        self.window.setReleasedWhenClosed_(False)
        
        # Title
        title = NSButton.alloc().initWithFrame_(NSMakeRect(20, 200, 360, 30))
        title.setTitle_("Choose Organization Methods:")
        title.setBordered_(False)
        title.setEnabled_(False)
        
        # Checkboxes
        self.type_cb = self._create_checkbox(
            40, 160, "By File Type (images, documents, software, etc.)",
            self.app.config.is_organize_by_type(), "toggleType:"
        )
        
        self.size_cb = self._create_checkbox(
            40, 130, "By File Size (small, medium, large)",
            self.app.config.is_organize_by_size(), "toggleSize:"
        )
        
        self.date_cb = self._create_checkbox(
            40, 100, "By Date Added (10-2025, 09-2025, etc.)",
            self.app.config.is_organize_by_date(), "toggleDate:"
        )
        
        # Info
        info = NSButton.alloc().initWithFrame_(NSMakeRect(40, 50, 340, 40))
        info.setTitle_("Multiple methods create nested folders\n(e.g., images/small/10-2025/)")
        info.setBordered_(False)
        info.setEnabled_(False)
        
        # Done button
        done = NSButton.alloc().initWithFrame_(NSMakeRect(150, 10, 100, 32))
        done.setTitle_("Done")
        done.setBezelStyle_(1)
        done.setTarget_(self)
        done.setAction_("close:")
        
        # Add all views
        for view in [title, self.type_cb, self.size_cb, self.date_cb, info, done]:
            self.window.contentView().addSubview_(view)
        
        self.window.makeKeyAndOrderFront_(None)
    
    def _create_checkbox(self, x, y, title, checked, action):
        """Helper to create a checkbox"""
        checkbox = NSButton.alloc().initWithFrame_(NSMakeRect(x, y, 340, 25))
        checkbox.setTitle_(title)
        checkbox.setButtonType_(NSButtonTypeSwitch)
        checkbox.setState_(1 if checked else 0)
        checkbox.setTarget_(self)
        checkbox.setAction_(action)
        return checkbox
    
    def toggleType_(self, sender):
        self.app.config.set_organize_by_type(sender.state() == 1)
    
    def toggleSize_(self, sender):
        self.app.config.set_organize_by_size(sender.state() == 1)
    
    def toggleDate_(self, sender):
        self.app.config.set_organize_by_date(sender.state() == 1)
    
    def close_(self, sender):
        self.window.close()


class AutoShelf(rumps.App):
    """Main application class"""
    
    def __init__(self):
        super().__init__("AutoShelf")
        self.icon = "logo.png"
        self.config = get_config()
        self.organizer = get_organizer()
        self.settings_window = None
        self.log_window = None
        
        # Create menu
        self._setup_menu()
        
        # Update UI
        self.update_toggle()
        self.update_organize_button()
        
        # Show tutorial for new users
        if self.config.should_show_tutorial():
            self.show_tutorial()
    
    def _setup_menu(self):
        """Setup the menu bar items"""
        self.toggle_btn = rumps.MenuItem("Auto-Organize New Files", callback=self.toggle)
        self.organize_btn = rumps.MenuItem("", callback=self.organize_existing)
        
        folder_submenu = [
            rumps.MenuItem("Downloads", callback=lambda _: self.set_folder("Downloads")),
            rumps.MenuItem("Documents", callback=lambda _: self.set_folder("Documents")),
            rumps.MenuItem("Desktop", callback=lambda _: self.set_folder("Desktop")),
            None,
            rumps.MenuItem("Choose...", callback=self.choose_folder),
        ]
        
        self.menu = [
            rumps.MenuItem("Settings", callback=self.show_settings),
            None,
            self.toggle_btn,
            self.organize_btn,
            ("Watch Folder", folder_submenu),
            None,
            rumps.MenuItem("Show Logs", callback=self.show_logs),
            rumps.MenuItem("How to Use", callback=lambda _: self.show_tutorial()),
            rumps.MenuItem("About", callback=self.show_about),
        ]
    
    def show_settings(self, _):
        if not self.settings_window:
            self.settings_window = SettingsWindow.alloc().initWithApp_(self)
        self.settings_window.showWindow()
    
    def show_logs(self, _):
        if not self.log_window:
            self.log_window = LogWindow.alloc().initWithApp_(self)
        self.log_window.showWindow()
    
    def show_tutorial(self):
        """Interactive tutorial for first-time users"""
        
        # Welcome
        if not rumps.alert(
            title="Welcome to AutoShelf! 📂",
            message="Automatically organize your files by type, size, and date.\n\nLet's get started!",
            icon_path=self.icon,
            ok="Next",
            cancel="Skip"
        ):
            self.config.set_tutorial_shown()
            return
        
        # Settings explanation
        if not rumps.alert(
            title="Choose Organization Methods",
            message="Open 'Settings' to choose:\n\n• By File Type\n• By File Size\n• By Date Added\n\nEnable one or more methods!",
            icon_path=self.icon,
            ok="Next",
            cancel="Skip"
        ):
            self.config.set_tutorial_shown()
            return
        
        # Auto-organize explanation
        if not rumps.alert(
            title="Enable Auto-Organize? 🚀",
            message=f"Start watching your {Path(self.config.get_watch_path()).name} folder?\n\nNew files will be automatically organized.\n\nYou can start/stop anytime from the menu.",
            icon_path=self.icon,
            ok="Yes, Start Now!",
            cancel="Not Yet"
        ):
            self.config.set_tutorial_shown()
            return
        
        # Start if user agreed
        self.organizer.start()
        self.update_toggle()
        rumps.notification("AutoShelf", "Enabled! 🎉", f"Watching: {Path(self.config.get_watch_path()).name}")
        self.config.set_tutorial_shown()
    
    def show_about(self, _):
        about = f"""AutoShelf v{__version__}

A smart macOS file organizer

Created by: {__author__}
License: MIT (Open Source)
GitHub: {__url__}

Features:
• Organize by type, size, and date
• Real-time monitoring
• Native macOS interface

Made with ❤️ for productivity"""
        
        rumps.alert(title="About AutoShelf", message=about, ok="Close")
    
    def toggle(self, _):
        if self.organizer.is_running():
            self.organizer.stop()
            rumps.notification("AutoShelf", "Stopped", "File monitoring OFF")
        else:
            self.organizer.start()
            folder_name = Path(self.config.get_watch_path()).name
            rumps.notification("AutoShelf", "Started!", f"Watching: {folder_name}")
        self.update_toggle()
    
    def set_folder(self, name):
        path = Path.home() / name
        path.mkdir(exist_ok=True)
        self.organizer.set_watch_path(str(path))
    
    def choose_folder(self, _):
        panel = NSOpenPanel.openPanel()
        panel.setCanChooseFiles_(False)
        panel.setCanChooseDirectories_(True)
        panel.setDirectoryURL_(NSURL.fileURLWithPath_(self.config.get_watch_path()))
        
        if panel.runModal() == 1:
            self.organizer.set_watch_path(panel.URL().path())
    
    def organize_existing(self, _):
        count = self.organizer.organize_existing_files()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config.set_last_organize(timestamp)
        self.update_organize_button()
        
        if count > 0:
            rumps.notification("AutoShelf", "Done!", f"Organized {count} file(s)")
        else:
            rumps.notification("AutoShelf", "No Files", "Nothing to organize")
    
    def update_organize_button(self):
        last = self.config.get_last_organize()
        if last:
            self.organize_btn.title = f"Organize Existing (Last: {last})"
        else:
            self.organize_btn.title = "Organize Existing Files"
    
    def update_toggle(self):
        if self.organizer.is_running():
            self.toggle_btn.title = "⬤ Stop Auto-Organize"
        else:
            self.toggle_btn.title = "Auto-Organize New Files"


if __name__ == "__main__":
    AutoShelf().run()
