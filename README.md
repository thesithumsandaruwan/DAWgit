# DawGit - A Simple Git GUI for Beginners

DawGit is a user-friendly Git GUI application designed to make Git accessible for everyone, especially those who are not familiar with command-line interfaces. With DawGit, you can perform all essential Git operations through a simple and intuitive interface.

## Features

- Create or open Git repositories
- View and manage file changes (stage, unstage)
- Commit changes with descriptive messages
- View commit history with detailed information
- Connect to remote repositories
- Push and pull changes easily
- Built-in help and guidance

## Download and Installation

### Windows Executable
1. Go to the [Releases](https://github.com/yourusername/dawgit/releases) page
2. Download the latest `DawGit-windows.zip` file
3. Extract the ZIP file
4. Run `DawGit.exe`

No installation required! Just make sure you have Git installed on your system.

### From Source
If you prefer to run from source:

1. Make sure you have Git and Python 3.6+ installed
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/dawgit.git
   cd dawgit
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python dawgit.py
   ```

## Building the Executable Yourself

If you want to build the executable yourself:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Build the executable:
   ```
   python setup.py build
   ```
3. The executable will be created in the `build/exe.win-*` directory

## Usage Guide

### Getting Started

1. **Opening or Creating a Repository**:
   - Click "Browse" to select an existing Git repository
   - Click "Create New Repo" to initialize a new Git repository

2. **Viewing and Managing Changes**:
   - The "Changes" tab shows both unstaged and staged changes
   - Select files and use "Stage Selected" or "Stage All" to prepare them for commit
   - Enter a commit message and click "Commit" to save your changes

3. **Viewing History**:
   - The "History" tab shows all previous commits
   - Click on a commit to see detailed information

4. **Working with Remote Repositories**:
   - In the "Remote" tab, enter a repository URL and click "Add Remote"
   - Use "Push" to send your commits to the remote repository
   - Use "Pull" to get the latest changes

5. **Getting Help**:
   - The "Help" tab provides guidance on using Git and the application

## For Beginners

If you're new to Git, DawGit simplifies the process by handling the complex commands behind the scenes. Here's a typical workflow:

1. Make changes to your files in any editor
2. Open DawGit and see your changes in the "Changes" tab
3. Stage the changes you want to commit
4. Enter a descriptive message and commit
5. Push your changes to share them with others

No need to remember complex command-line instructions - everything is just a click away!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.