import sys
import os
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["os", "tkinter", "git", "gitdb", "smmap"],
    "includes": ["tkinter", "tkinter.ttk"],
    "include_files": ["README.md", "LICENSE"],
    "excludes": [],
    "include_msvcr": True
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
        target_name="DawGit.exe"
    )]
)