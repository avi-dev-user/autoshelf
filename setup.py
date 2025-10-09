"""
Setup script for building AutoShelf.app with py2app
"""
from setuptools import setup
from version import __version__

APP = ['main.py']
DATA_FILES = [
    ('', ['logo.png']),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'logo.png',
    'plist': {
        'CFBundleName': 'AutoShelf',
        'CFBundleDisplayName': 'AutoShelf',
        'CFBundleGetInfoString': "Smart File Organizer",
        'CFBundleIdentifier': 'com.amirmghanem.autoshelf',
        'CFBundleVersion': __version__,
        'CFBundleShortVersionString': __version__,
        'LSUIElement': True,
        'NSHighResolutionCapable': True,
    },
    'packages': ['rumps', 'watchdog', 'pync'],
    'includes': ['config', 'auto_organizer', 'version'],
    'excludes': ['pytest', 'setuptools', 'pip'],
}

setup(
    name='AutoShelf',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version=__version__,
)

