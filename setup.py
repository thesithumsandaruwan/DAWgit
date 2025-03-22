import sys
import os
from cx_Freeze import setup, Executable

# Define paths to exclude
path_excludes = [
    "C:\\Users\\Acer\\AppData\\Local\\Microsoft\\WindowsApps",
    "C:\\Users\\SS5\\AppData\\Local\\Microsoft\\WindowsApps"
]

# Dependencies
build_exe_options = {
    "packages": ["os", "tkinter", "git", "gitdb", "smmap"],
    "includes": ["tkinter", "tkinter.ttk"],
    "include_files": ["README.md", "LICENSE"],
    "excludes": [],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
    "path": [p for p in sys.path if p not in path_excludes]
}

# Base for Windows application without console
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="DawGit",
    version="1.0.0",
    description="A Simple Git GUI for Beginners",
    author="DawGit",
    options={"build_exe": build_exe_options},
    executables=[Executable(
        script="dawgit.py",
        base=base,
        target_name="DawGit.exe",
        icon=None,
        copyright="Copyright (c) 2025 DawGit"
    )]
)