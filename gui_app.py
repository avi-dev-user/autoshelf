#!/usr/bin/env python3
"""
AutoShelf Linux GUI Application
Cross-platform file organizer with a modern GUI interface
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
import queue
from pathlib import Path
from datetime import datetime
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import get_config
from auto_organizer import get_organizer, log
from version import __version__, __author__, __url__


class ModernButton(tk.Button):
    """Modern looking button widget"""
    def __init__(self, parent, **kwargs):
        # Set modern styling defaults
        defaults = {
            'relief': 'flat',
            'bd': 0,
            'padx': 20,
            'pady': 8,
            'bg': '#007ACC',
            'fg': 'white',
            'font': ('Arial', 10),
            'cursor': 'hand2'
        }
        defaults.update(kwargs)
        super().__init__(parent, **defaults)
        
        # Hover effects
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.original_bg = defaults['bg']
    
    def _on_enter(self, e):
        self.config(bg='#005A9E')
    
    def _on_leave(self, e):
        self.config(bg=self.original_bg)


class LogWindow:
    """Live log viewer window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.text_widget = None
        self.log_queue = queue.Queue()
        
    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent.root)
        self.window.title("AutoShelf - Live Logs")
        self.window.geometry("800x500")
        self.window.iconbitmap() if hasattr(self.window, 'iconbitmap') else None
        
        # Create widgets
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log text area
        self.text_widget = scrolledtext.ScrolledText(
            frame, 
            wrap=tk.WORD, 
            font=('Consolas', 10),
            bg='#1E1E1E',
            fg='#FFFFFF',
            insertbackground='white'
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        clear_btn = ModernButton(
            btn_frame, 
            text="Clear Logs",
            command=self.clear_logs,
            bg='#DC3545'
        )
        clear_btn.pack(side=tk.LEFT)
        
        refresh_btn = ModernButton(
            btn_frame,
            text="Refresh", 
            command=self.refresh_logs,
            bg='#28A745'
        )
        refresh_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Start auto-refresh
        self.refresh_logs()
        self.window.after(1000, self._auto_refresh)
    
    def _auto_refresh(self):
        if self.window and self.window.winfo_exists():
            self.refresh_logs()
            self.window.after(1000, self._auto_refresh)
    
    def refresh_logs(self):
        if not self.text_widget:
            return
            
        # Get logs from organizer (we'll need to modify the log system)
        try:
            self.text_widget.delete(1.0, tk.END)
            # For now, show a placeholder - we'll implement proper logging later
            logs = "AutoShelf Linux - Logs will appear here...\n"
            self.text_widget.insert(tk.END, logs)
            self.text_widget.see(tk.END)
        except:
            pass
    
    def clear_logs(self):
        if self.text_widget:
            self.text_widget.delete(1.0, tk.END)


class SettingsWindow:
    """Settings configuration window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.config = get_config()
        
    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent.root)
        self.window.title("Organization Settings")
        self.window.geometry("450x350")
        self.window.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Choose Organization Methods:",
            font=('Arial', 14, 'bold'),
            fg='#333333'
        )
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Checkboxes frame
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create checkbox variables
        self.type_var = tk.BooleanVar(value=self.config.is_organize_by_type())
        self.size_var = tk.BooleanVar(value=self.config.is_organize_by_size())
        self.date_var = tk.BooleanVar(value=self.config.is_organize_by_date())
        
        # Checkboxes
        type_cb = tk.Checkbutton(
            options_frame,
            text="📂 By File Type (images, documents, software, etc.)",
            variable=self.type_var,
            font=('Arial', 11),
            command=self._update_config
        )
        type_cb.pack(anchor=tk.W, pady=5)
        
        size_cb = tk.Checkbutton(
            options_frame,
            text="📊 By File Size (small, medium, large)",
            variable=self.size_var,
            font=('Arial', 11),
            command=self._update_config
        )
        size_cb.pack(anchor=tk.W, pady=5)
        
        date_cb = tk.Checkbutton(
            options_frame,
            text="📅 By Date Added (10-2025, 09-2025, etc.)",
            variable=self.date_var,
            font=('Arial', 11),
            command=self._update_config
        )
        date_cb.pack(anchor=tk.W, pady=5)
        
        # Info text
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 20))
        
        info_label = tk.Label(
            info_frame,
            text="💡 Multiple methods create nested folders\n(e.g., images/small/10-2025/)",
            font=('Arial', 10),
            fg='#666666',
            justify=tk.LEFT
        )
        info_label.pack(anchor=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        done_btn = ModernButton(
            btn_frame,
            text="Done",
            command=self.window.destroy,
            bg='#28A745'
        )
        done_btn.pack(side=tk.RIGHT)
        
        apply_btn = ModernButton(
            btn_frame,
            text="Apply & Save",
            command=self._save_and_notify,
            bg='#007ACC'
        )
        apply_btn.pack(side=tk.RIGHT, padx=(0, 10))
    
    def _update_config(self):
        """Update configuration when checkboxes change"""
        self.config.set_organize_by_type(self.type_var.get())
        self.config.set_organize_by_size(self.size_var.get())
        self.config.set_organize_by_date(self.date_var.get())
    
    def _save_and_notify(self):
        """Save configuration and show confirmation"""
        self._update_config()
        messagebox.showinfo("Settings", "Configuration saved successfully!")


class AutoShelfGUI:
    """Main AutoShelf GUI Application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.config = get_config()
        self.organizer = get_organizer()
        self.settings_window = None
        self.log_window = None
        
        # Set up the main window
        self._setup_window()
        self._create_widgets()
        self._update_ui()
        
        # Check for first run tutorial
        if self.config.should_show_tutorial():
            self.root.after(500, self.show_tutorial)
    
    def _setup_window(self):
        """Configure the main window"""
        self.root.title(f"AutoShelf v{__version__}")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Try to set icon if available
        try:
            icon_path = Path(__file__).parent / "logo.png"
            if icon_path.exists():
                # Convert to PhotoImage if needed (Linux doesn't support PNG directly)
                pass
        except:
            pass
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"500x600+{x}+{y}")
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = tk.Label(
            header_frame,
            text="📂 AutoShelf",
            font=('Arial', 24, 'bold'),
            fg='#2C3E50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Smart file organization for Linux",
            font=('Arial', 12),
            fg='#7F8C8D'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="⏸️ Monitoring: Stopped",
            font=('Arial', 12, 'bold'),
            fg='#E74C3C'
        )
        self.status_label.pack(anchor=tk.W)
        
        self.folder_label = tk.Label(
            status_frame,
            text=f"📁 Watching: {Path(self.config.get_watch_path()).name}",
            font=('Arial', 10),
            fg='#34495E'
        )
        self.folder_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Controls section
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding=15)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Start/Stop button
        self.toggle_btn = ModernButton(
            controls_frame,
            text="▶️ Start Auto-Organization",
            command=self.toggle_monitoring,
            bg='#27AE60',
            font=('Arial', 12, 'bold')
        )
        self.toggle_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Organize existing button
        self.organize_btn = ModernButton(
            controls_frame,
            text="📦 Organize Existing Files",
            command=self.organize_existing,
            bg='#3498DB'
        )
        self.organize_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Settings button
        settings_btn = ModernButton(
            controls_frame,
            text="⚙️ Settings",
            command=self.show_settings,
            bg='#9B59B6'
        )
        settings_btn.pack(fill=tk.X)
        
        # Folder selection section
        folder_frame = ttk.LabelFrame(main_frame, text="Watch Folder", padding=15)
        folder_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Quick folder buttons
        quick_frame = ttk.Frame(folder_frame)
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        for folder_name in ["Downloads", "Documents", "Desktop"]:
            btn = ModernButton(
                quick_frame,
                text=folder_name,
                command=lambda f=folder_name: self.set_quick_folder(f),
                bg='#95A5A6'
            )
            btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Custom folder button
        custom_btn = ModernButton(
            folder_frame,
            text="📁 Choose Custom Folder...",
            command=self.choose_folder,
            bg='#E67E22'
        )
        custom_btn.pack(fill=tk.X)
        
        # Tools section
        tools_frame = ttk.LabelFrame(main_frame, text="Tools", padding=15)
        tools_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logs button
        logs_btn = ModernButton(
            tools_frame,
            text="📋 Show Live Logs",
            command=self.show_logs,
            bg='#34495E'
        )
        logs_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # About button
        about_btn = ModernButton(
            tools_frame,
            text="ℹ️ About",
            command=self.show_about,
            bg='#16A085'
        )
        about_btn.pack(side=tk.LEFT)
        
        # Tutorial button
        help_btn = ModernButton(
            tools_frame,
            text="❓ Tutorial",
            command=self.show_tutorial,
            bg='#F39C12'
        )
        help_btn.pack(side=tk.RIGHT)
    
    def _update_ui(self):
        """Update UI elements based on current state"""
        is_running = self.organizer.is_running()
        
        # Update status
        if is_running:
            self.status_label.config(
                text="▶️ Monitoring: Active",
                fg='#27AE60'
            )
            self.toggle_btn.config(
                text="⏸️ Stop Auto-Organization",
                bg='#E74C3C'
            )
        else:
            self.status_label.config(
                text="⏸️ Monitoring: Stopped", 
                fg='#E74C3C'
            )
            self.toggle_btn.config(
                text="▶️ Start Auto-Organization",
                bg='#27AE60'
            )
        
        # Update folder label
        folder_path = Path(self.config.get_watch_path())
        self.folder_label.config(text=f"📁 Watching: {folder_path.name}")
        
        # Update organize button
        last = self.config.get_last_organize()
        if last:
            self.organize_btn.config(text=f"📦 Organize Existing (Last: {last})")
        else:
            self.organize_btn.config(text="📦 Organize Existing Files")
    
    def toggle_monitoring(self):
        """Start or stop file monitoring"""
        try:
            if self.organizer.is_running():
                self.organizer.stop()
                self._show_notification("AutoShelf", "File monitoring stopped", "info")
            else:
                # Check if any organization method is enabled
                if not (self.config.is_organize_by_type() or 
                       self.config.is_organize_by_size() or 
                       self.config.is_organize_by_date()):
                    messagebox.showwarning(
                        "No Organization Methods", 
                        "Please enable at least one organization method in Settings first!"
                    )
                    return
                
                self.organizer.start()
                folder_name = Path(self.config.get_watch_path()).name
                self._show_notification("AutoShelf", f"Monitoring started for: {folder_name}", "info")
            
            self._update_ui()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle monitoring: {e}")
    
    def organize_existing(self):
        """Organize all existing files in the watch folder"""
        try:
            # Check if any organization method is enabled
            if not (self.config.is_organize_by_type() or 
                   self.config.is_organize_by_size() or 
                   self.config.is_organize_by_date()):
                messagebox.showwarning(
                    "No Organization Methods", 
                    "Please enable at least one organization method in Settings first!"
                )
                return
            
            # Run in background thread to avoid UI freeze
            def run_organize():
                try:
                    count = self.organizer.organize_existing_files()
                    
                    # Update last organize time
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.config.set_last_organize(timestamp)
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self._on_organize_complete(count))
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Organization failed: {e}"))
            
            threading.Thread(target=run_organize, daemon=True).start()
            
            # Show progress dialog
            messagebox.showinfo("Organizing", "Organizing files... This may take a moment.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to organize files: {e}")
    
    def _on_organize_complete(self, count):
        """Called when organization is complete"""
        self._update_ui()
        if count > 0:
            self._show_notification("AutoShelf", f"Organized {count} file(s)", "info")
        else:
            self._show_notification("AutoShelf", "No files to organize", "info")
    
    def set_quick_folder(self, folder_name):
        """Set watch folder to a quick preset"""
        try:
            folder_path = Path.home() / folder_name
            folder_path.mkdir(exist_ok=True)
            
            # Stop monitoring if running
            was_running = self.organizer.is_running()
            if was_running:
                self.organizer.stop()
            
            # Set new path
            self.organizer.set_watch_path(str(folder_path))
            
            # Restart if it was running
            if was_running:
                self.organizer.start()
            
            self._update_ui()
            self._show_notification("AutoShelf", f"Now watching: {folder_name}", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set folder: {e}")
    
    def choose_folder(self):
        """Choose a custom watch folder"""
        try:
            folder = filedialog.askdirectory(
                title="Choose folder to watch",
                initialdir=self.config.get_watch_path()
            )
            
            if folder:
                # Stop monitoring if running
                was_running = self.organizer.is_running()
                if was_running:
                    self.organizer.stop()
                
                # Set new path
                self.organizer.set_watch_path(folder)
                
                # Restart if it was running
                if was_running:
                    self.organizer.start()
                
                self._update_ui()
                self._show_notification("AutoShelf", f"Now watching: {Path(folder).name}", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set folder: {e}")
    
    def show_settings(self):
        """Show settings window"""
        if not self.settings_window:
            self.settings_window = SettingsWindow(self)
        self.settings_window.show()
    
    def show_logs(self):
        """Show log window"""
        if not self.log_window:
            self.log_window = LogWindow(self)
        self.log_window.show()
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""AutoShelf v{__version__} (Linux Edition)

A smart file organizer for Linux desktops

Features:
• Organize by file type, size, and date
• Real-time monitoring
• Modern GUI interface
• Cross-platform compatibility

Created by: {__author__}
License: MIT (Open Source)
Website: {__url__}

Made with ❤️ for productivity"""
        
        messagebox.showinfo("About AutoShelf", about_text)
    
    def show_tutorial(self):
        """Show interactive tutorial"""
        steps = [
            ("Welcome to AutoShelf! 📂", 
             "AutoShelf automatically organizes your files by type, size, and date.\n\nLet's get started!"),
            
            ("Choose Organization Methods ⚙️", 
             "Click 'Settings' to choose how to organize your files:\n\n• By File Type (images, documents, etc.)\n• By File Size (small, medium, large)\n• By Date Added (monthly folders)\n\nYou can enable multiple methods!"),
            
            ("Start Monitoring 🚀", 
             "Ready to start?\n\n1. Make sure at least one organization method is enabled\n2. Choose your watch folder (Downloads is default)\n3. Click 'Start Auto-Organization'\n\nNew files will be organized automatically!"),
            
            ("Additional Features 🔧", 
             "Other useful features:\n\n• 'Organize Existing Files' - organize files already in the folder\n• 'Show Live Logs' - see what's happening in real-time\n• 'Choose Custom Folder' - watch any folder you want\n\nEnjoy your organized files! 🎉")
        ]
        
        for title, message in steps:
            result = messagebox.askokcancel(title, message)
            if not result:
                break
        
        # Mark tutorial as shown
        self.config.set_tutorial_shown()
    
    def _show_notification(self, title, message, type_="info"):
        """Show desktop notification (Linux compatible)"""
        try:
            # Try using native Linux notifications
            os.system(f'notify-send "{title}" "{message}"')
        except:
            # Fallback to tkinter messagebox
            if type_ == "info":
                messagebox.showinfo(title, message)
            elif type_ == "warning":
                messagebox.showwarning(title, message)
            elif type_ == "error":
                messagebox.showerror(title, message)
    
    def _on_closing(self):
        """Handle application closing"""
        try:
            # Stop monitoring
            if self.organizer.is_running():
                self.organizer.stop()
            
            # Close all windows
            self.root.quit()
            self.root.destroy()
        except:
            pass
    
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_closing()


def main():
    """Main entry point for Linux GUI version"""
    print("Starting AutoShelf Linux GUI...")
    app = AutoShelfGUI()
    app.run()


if __name__ == "__main__":
    main()
