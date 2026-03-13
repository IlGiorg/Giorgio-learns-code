"""
setup.py - Build script for py2app
Run: python setup.py py2app
"""

from setuptools import setup

APP = ['version5.py']  # Your main file name
DATA_FILES = []  # Add any data files here if needed

OPTIONS = {
    'argv_emulation': False,
    'packages': ['tkinter', 'sqlite3', 'json', 'random', 'math', 'time', 'datetime'],
    'includes': ['tkinter', 'sqlite3', 'json'],
    'excludes': ['PyQt5', 'PySide2', 'matplotlib', 'numpy'],
    'plist': {
        'CFBundleName': 'CS Flashcard Game',
        'CFBundleDisplayName': 'CS Flashcard Game',
        'CFBundleGetInfoString': 'Learn Computer Science with Flashcards',
        'CFBundleIdentifier': 'com.yourname.csflashcard',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0.0',
        'CFBundleIconFile': 'icon.icns',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
        'LSMinimumSystemVersion': '10.10.0',
    },
    'iconfile': 'icon.icns',  # You'll create this next
}

setup(
    name='CS Flashcard Game',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)