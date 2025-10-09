# Contributing to AutoShelf 🤝

First off, thank you for considering contributing to AutoShelf! It's people like you that make AutoShelf such a great tool.

## Code of Conduct

Be respectful, inclusive, and considerate. We're all here to make file organization better!

## How Can I Contribute?

### 🐛 Reporting Bugs

**Before submitting a bug report:**
- Check if the bug has already been reported in [Issues](https://github.com/amirmghanem/autoshelf/issues)
- Try with the latest version
- Check if it's a known limitation in the README

**When submitting a bug report, include:**
- **macOS version** (e.g., macOS 14.0 Sonoma)
- **Python version** (`python --version`)
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Log output** (from "Show Logs" menu)
- **Screenshots** if applicable

### ✨ Suggesting Features

**Before suggesting a feature:**
- Check if it's already suggested in [Issues](https://github.com/amirmghanem/autoshelf/issues)
- Consider if it aligns with the project's goal: **simplicity and ease of use**

**When suggesting a feature:**
- Use a clear, descriptive title
- Explain **why** this feature would be useful
- Describe **how** it should work
- Include mockups or examples if relevant

### 🔧 Pull Requests

**Development Process:**

1. **Fork** the repo
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/autoshelf.git
   cd autoshelf
   ```

3. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv/bin/activate.fish for fish shell
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

6. **Make your changes**

7. **Test your changes:**
   ```bash
   python main.py
   ```

8. **Commit:**
   ```bash
   git commit -m "Add feature: brief description"
   ```

9. **Push:**
   ```bash
   git push origin feature/your-feature-name
   ```

10. **Open a Pull Request** on GitHub

## Code Style Guidelines

### Python Style
- **PEP 8** compliant (mostly)
- **Simple is better than complex**
- Use descriptive variable names
- Add docstrings for classes and complex functions

### Keep It Simple
AutoShelf's philosophy is simplicity:
- Avoid unnecessary dependencies
- Keep the UI clean and intuitive
- Minimize configuration options
- Make it "just work"

### Examples of Good Contributions:
✅ Adding support for new file types
✅ Improving categorization logic
✅ Bug fixes
✅ Performance improvements
✅ Better logging
✅ UI enhancements (keeping it simple)

### Examples to Avoid:
❌ Adding complex configuration systems
❌ Introducing heavy dependencies
❌ Over-engineering simple features
❌ Breaking existing functionality

## Project Structure

```
autoshelf/
├── main.py              # Main app, UI, menu bar
├── auto_organizer.py    # File watcher and organization logic
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── logo.png            # App icon
└── README.md           # Documentation
```

## Testing

**Manual Testing Checklist:**
- [ ] App starts without errors
- [ ] Settings window opens and saves correctly
- [ ] Files are organized correctly by type
- [ ] Files are organized correctly by size
- [ ] Files are organized correctly by date
- [ ] Multiple methods work together (nested folders)
- [ ] Start/Stop toggle works
- [ ] "Organize Existing" processes all files
- [ ] Logs display correctly
- [ ] Folder picker works
- [ ] App doesn't crash on edge cases

**Test on a clean environment:**
```bash
# Create test folder
mkdir ~/test_autoshelf
cd ~/test_autoshelf

# Create various test files
touch test.jpg test.pdf bigfile.zip code.py

# Run AutoShelf pointed at this folder
```

## Adding New File Types

To add support for a new file type, edit `auto_organizer.py`:

```python
def categorize_by_type(self, file_path):
    # ... existing code ...
    
    # Your new category
    if ext in ['.new', '.ext']:
        return "yourcategory"
```

## Commit Message Guidelines

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Move file" not "Moves file"
- Keep first line under 72 characters
- Reference issues: "Fix #123: Description"

**Examples:**
```
✅ Add support for .heic image files
✅ Fix crash when folder doesn't exist
✅ Improve date formatting in logs
❌ fixed a bug
❌ WIP - testing stuff
```

## Questions?

- Open an [issue](https://github.com/amirmghanem/autoshelf/issues) for questions
- Tag with `question` label
- Check existing issues first

## Recognition

Contributors will be added to this README! 🎉

Thank you for making AutoShelf better! 🙌

