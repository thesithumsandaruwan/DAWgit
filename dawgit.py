import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import git
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

class DawGitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DawGit - Simple Git GUI")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Set theme colors
        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.accent_color = "#4CAF50"
        self.button_color = "#e7e7e7"
        
        # Initialize repository
        self.repo = None
        self.repo_path = None
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create and configure widgets
        self.create_widgets()
        
        # Update status
        self.update_status("Ready. Please open or create a repository.")
    
    def create_widgets(self):
        # Create header frame
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # App title and description
        title_label = ttk.Label(header_frame, text="DawGit", font=("Arial", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        desc_label = ttk.Label(header_frame, text="A simple Git GUI for beginners")
        desc_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
        
        # Repository selection frame
        repo_frame = ttk.LabelFrame(self.main_frame, text="Repository")
        repo_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.repo_path_var = tk.StringVar()
        repo_path_entry = ttk.Entry(repo_frame, textvariable=self.repo_path_var, width=50)
        repo_path_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(repo_frame, text="Browse", command=self.browse_repository)
        browse_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        create_btn = ttk.Button(repo_frame, text="Create New Repo", command=self.create_repository)
        create_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create main content frame with tabs
        tab_control = ttk.Notebook(self.main_frame)
        
        # Changes tab
        changes_tab = ttk.Frame(tab_control)
        tab_control.add(changes_tab, text="Changes")
        self.setup_changes_tab(changes_tab)
        
        # History tab
        history_tab = ttk.Frame(tab_control)
        tab_control.add(history_tab, text="History")
        self.setup_history_tab(history_tab)
        
        # Remote tab
        remote_tab = ttk.Frame(tab_control)
        tab_control.add(remote_tab, text="Remote")
        self.setup_remote_tab(remote_tab)
        
        # Help tab
        help_tab = ttk.Frame(tab_control)
        tab_control.add(help_tab, text="Help")
        self.setup_help_tab(help_tab)
        
        tab_control.pack(expand=True, fill=tk.BOTH)
        
        # Status bar
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar()
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def setup_changes_tab(self, parent):
        # Create frames for staging and committing
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Unstaged changes section
        unstaged_frame = ttk.LabelFrame(main_frame, text="Unstaged Changes")
        unstaged_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=(0, 5))
        
        self.unstaged_listbox = tk.Listbox(unstaged_frame, selectmode=tk.MULTIPLE)
        self.unstaged_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        unstaged_scrollbar = ttk.Scrollbar(unstaged_frame)
        unstaged_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.unstaged_listbox.config(yscrollcommand=unstaged_scrollbar.set)
        unstaged_scrollbar.config(command=self.unstaged_listbox.yview)
        
        # Buttons for staging
        stage_buttons_frame = ttk.Frame(main_frame)
        stage_buttons_frame.pack(fill=tk.X, pady=5)
        
        stage_selected_btn = ttk.Button(stage_buttons_frame, text="Stage Selected", command=self.stage_selected)
        stage_selected_btn.pack(side=tk.LEFT, padx=5)
        
        stage_all_btn = ttk.Button(stage_buttons_frame, text="Stage All", command=self.stage_all)
        stage_all_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(stage_buttons_frame, text="Refresh", command=self.refresh_repo_status)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Staged changes section
        staged_frame = ttk.LabelFrame(main_frame, text="Staged Changes")
        staged_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=5)
        
        self.staged_listbox = tk.Listbox(staged_frame, selectmode=tk.MULTIPLE)
        self.staged_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        staged_scrollbar = ttk.Scrollbar(staged_frame)
        staged_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.staged_listbox.config(yscrollcommand=staged_scrollbar.set)
        staged_scrollbar.config(command=self.staged_listbox.yview)
        
        # Unstage buttons
        unstage_buttons_frame = ttk.Frame(main_frame)
        unstage_buttons_frame.pack(fill=tk.X, pady=5)
        
        unstage_selected_btn = ttk.Button(unstage_buttons_frame, text="Unstage Selected", command=self.unstage_selected)
        unstage_selected_btn.pack(side=tk.LEFT, padx=5)
        
        unstage_all_btn = ttk.Button(unstage_buttons_frame, text="Unstage All", command=self.unstage_all)
        unstage_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Commit section
        commit_frame = ttk.LabelFrame(main_frame, text="Commit")
        commit_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        self.commit_msg = tk.Text(commit_frame, height=3)
        self.commit_msg.pack(fill=tk.X, padx=5, pady=5)
        
        commit_button = ttk.Button(commit_frame, text="Commit", command=self.commit_changes)
        commit_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def setup_history_tab(self, parent):
        # Create frame for commit history
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Commit history list
        history_frame = ttk.LabelFrame(main_frame, text="Commit History")
        history_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        
        self.history_listbox = tk.Listbox(history_frame)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        history_scrollbar = ttk.Scrollbar(history_frame)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_listbox.yview)
        
        # Commit details
        details_frame = ttk.LabelFrame(main_frame, text="Commit Details")
        details_frame.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM, pady=5)
        
        self.commit_details = scrolledtext.ScrolledText(details_frame, height=10)
        self.commit_details.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.history_listbox.bind('<<ListboxSelect>>', self.show_commit_details)
    
    def setup_remote_tab(self, parent):
        # Create frame for remote operations
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Remote section
        remote_frame = ttk.LabelFrame(main_frame, text="Remote Repository")
        remote_frame.pack(fill=tk.X, pady=5)
        
        self.remote_var = tk.StringVar()
        remote_entry = ttk.Entry(remote_frame, textvariable=self.remote_var, width=50)
        remote_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        add_remote_btn = ttk.Button(remote_frame, text="Add Remote", command=self.add_remote)
        add_remote_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Push/Pull section
        push_pull_frame = ttk.Frame(main_frame)
        push_pull_frame.pack(fill=tk.X, pady=10)
        
        pull_btn = ttk.Button(push_pull_frame, text="Pull", command=self.pull_changes)
        pull_btn.pack(side=tk.LEFT, padx=5)
        
        push_btn = ttk.Button(push_pull_frame, text="Push", command=self.push_changes)
        push_btn.pack(side=tk.LEFT, padx=5)
        
        # Remote log
        log_frame = ttk.LabelFrame(main_frame, text="Remote Operations Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.remote_log = scrolledtext.ScrolledText(log_frame)
        self.remote_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_help_tab(self, parent):
        # Create frame for help content
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = """
        DawGit - A Simple Git GUI for Beginners
        
        This application makes Git easy to use without complex commands!
        
        Basic Workflow:
        
        1. Open or create a repository using the buttons at the top
        2. Make changes to your files in your favorite editor
        3. On the "Changes" tab:
           - See your changes in "Unstaged Changes"
           - Click "Stage Selected" or "Stage All" to prepare them for commit
           - Write a commit message
           - Click "Commit" to save your changes
        
        4. On the "Remote" tab:
           - Add a remote repository URL if you haven't already
           - Click "Push" to send your changes to the remote repository
           - Click "Pull" to get the latest changes from the remote repository
        
        5. Use the "History" tab to view your previous commits
        
        Common Git Terms:
        - Repository: Your project folder that Git keeps track of
        - Staging: Preparing files for committing
        - Commit: Saving a snapshot of your changes
        - Push: Sending commits to a remote repository
        - Pull: Getting commits from a remote repository
        
        Need more help? Visit: https://git-scm.com/doc
        """
        
        help_text = scrolledtext.ScrolledText(main_frame)
        help_text.pack(fill=tk.BOTH, expand=True)
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  # Make it read-only
    
    def browse_repository(self):
        directory = filedialog.askdirectory(title="Select Git Repository")
        if directory:
            self.open_repository(directory)
    
    def create_repository(self):
        directory = filedialog.askdirectory(title="Create New Git Repository")
        if directory:
            try:
                # Create a new Git repository
                self.repo = Repo.init(directory)
                self.repo_path = directory
                self.repo_path_var.set(directory)
                self.update_status(f"Created and opened new repository at {directory}")
                self.refresh_repo_status()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create repository: {str(e)}")
    
    def open_repository(self, path):
        try:
            self.repo = Repo(path)
            self.repo_path = path
            self.repo_path_var.set(path)
            self.update_status(f"Opened repository: {path}")
            self.refresh_repo_status()
            self.refresh_history()
        except InvalidGitRepositoryError:
            response = messagebox.askyesno("Not a Git Repository", 
                                          f"{path} is not a Git repository. Would you like to initialize it as one?")
            if response:
                self.repo = Repo.init(path)
                self.repo_path = path
                self.repo_path_var.set(path)
                self.update_status(f"Initialized new repository at {path}")
                self.refresh_repo_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open repository: {str(e)}")
    
    def refresh_repo_status(self):
        if not self.repo:
            return
        
        # Clear current lists
        self.unstaged_listbox.delete(0, tk.END)
        self.staged_listbox.delete(0, tk.END)
        
        try:
            # Get repo status
            repo_status = self.repo.git.status('--porcelain')
            status_lines = repo_status.split('\n') if repo_status else []
            
            for line in status_lines:
                if not line.strip():
                    continue
                
                status_code = line[:2]
                file_path = line[3:]
                
                if status_code[0] == 'M' or status_code[0] == 'A' or status_code[0] == 'D':
                    # File is staged
                    self.staged_listbox.insert(tk.END, f"{status_code} {file_path}")
                
                if status_code[1] == 'M' or status_code == '??':
                    # File is unstaged or untracked
                    self.unstaged_listbox.insert(tk.END, f"{status_code} {file_path}")
            
            self.update_status("Repository status refreshed.")
        except Exception as e:
            self.update_status(f"Error refreshing repository status: {str(e)}")
    
    def refresh_history(self):
        if not self.repo or not self.repo.heads:
            return
        
        # Clear current history
        self.history_listbox.delete(0, tk.END)
        
        try:
            # Get commit history
            for commit in self.repo.iter_commits():
                commit_date = commit.committed_datetime.strftime("%Y-%m-%d %H:%M")
                commit_msg = commit.message.strip().split('\n')[0]  # First line of commit message
                self.history_listbox.insert(tk.END, f"{commit_date} - {commit_msg}")
            
            self.update_status("Commit history refreshed.")
        except Exception as e:
            self.update_status(f"Error refreshing commit history: {str(e)}")
    
    def show_commit_details(self, event):
        if not self.repo:
            return
        
        try:
            # Get selected commit
            selected_idx = self.history_listbox.curselection()
            if not selected_idx:
                return
            
            # Clear previous details
            self.commit_details.delete(1.0, tk.END)
            
            # Get commit from history
            commits = list(self.repo.iter_commits())
            commit = commits[selected_idx[0]]
            
            # Format commit details
            details = f"Commit: {commit.hexsha}\n"
            details += f"Author: {commit.author.name} <{commit.author.email}>\n"
            details += f"Date: {commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            details += f"Message:\n{commit.message}\n\n"
            
            # Get list of changed files
            diff_index = commit.diff(commit.parents[0] if commit.parents else None)
            details += "Changed files:\n"
            for diff in diff_index:
                details += f"- {diff.a_path}\n"
            
            self.commit_details.insert(tk.END, details)
        except Exception as e:
            self.commit_details.insert(tk.END, f"Error loading commit details: {str(e)}")
    
    def stage_selected(self):
        if not self.repo:
            return
        
        selected_items = self.unstaged_listbox.curselection()
        if not selected_items:
            messagebox.showinfo("Info", "No files selected to stage.")
            return
        
        try:
            for idx in selected_items:
                item = self.unstaged_listbox.get(idx)
                file_path = item[3:]  # Remove status code and space
                self.repo.git.add(file_path)
            
            self.update_status("Selected files staged.")
            self.refresh_repo_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stage files: {str(e)}")
    
    def stage_all(self):
        if not self.repo:
            return
        
        try:
            self.repo.git.add(A=True)
            self.update_status("All changes staged.")
            self.refresh_repo_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stage all files: {str(e)}")
    
    def unstage_selected(self):
        if not self.repo:
            return
        
        selected_items = self.staged_listbox.curselection()
        if not selected_items:
            messagebox.showinfo("Info", "No files selected to unstage.")
            return
        
        try:
            for idx in selected_items:
                item = self.staged_listbox.get(idx)
                file_path = item[3:]  # Remove status code and space
                self.repo.git.reset("HEAD", file_path)
            
            self.update_status("Selected files unstaged.")
            self.refresh_repo_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unstage files: {str(e)}")
    
    def unstage_all(self):
        if not self.repo:
            return
        
        try:
            self.repo.git.reset("HEAD")
            self.update_status("All changes unstaged.")
            self.refresh_repo_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unstage all files: {str(e)}")
    
    def commit_changes(self):
        if not self.repo:
            return
        
        commit_message = self.commit_msg.get("1.0", tk.END).strip()
        if not commit_message:
            messagebox.showinfo("Info", "Please enter a commit message.")
            return
        
        try:
            self.repo.git.commit(m=commit_message)
            self.update_status("Changes committed successfully.")
            self.commit_msg.delete("1.0", tk.END)
            self.refresh_repo_status()
            self.refresh_history()
        except GitCommandError as e:
            if "nothing to commit" in str(e):
                messagebox.showinfo("Info", "No changes staged for commit.")
            else:
                messagebox.showerror("Error", f"Failed to commit changes: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to commit changes: {str(e)}")
    
    def add_remote(self):
        if not self.repo:
            return
        
        remote_url = self.remote_var.get().strip()
        if not remote_url:
            messagebox.showinfo("Info", "Please enter a remote repository URL.")
            return
        
        try:
            # Check if 'origin' remote already exists
            existing_remotes = [remote.name for remote in self.repo.remotes]
            
            if 'origin' in existing_remotes:
                # Update existing remote
                self.repo.git.remote('set-url', 'origin', remote_url)
                message = "Updated remote 'origin'"
            else:
                # Add new remote
                self.repo.git.remote('add', 'origin', remote_url)
                message = "Added remote 'origin'"
            
            self.update_status(f"{message} with URL: {remote_url}")
            self.remote_log.insert(tk.END, f"{message} with URL: {remote_url}\n")
        except Exception as e:
            error_message = f"Failed to add/update remote: {str(e)}"
            self.update_status(error_message)
            self.remote_log.insert(tk.END, f"ERROR: {error_message}\n")
    
    def pull_changes(self):
        if not self.repo:
            return
        
        try:
            # Check if remote exists
            if not self.repo.remotes:
                messagebox.showinfo("Info", "No remote repository configured. Please add a remote first.")
                return
            
            # Pull changes
            pull_info = self.repo.git.pull()
            self.update_status("Pull completed successfully.")
            self.remote_log.insert(tk.END, f"Pull completed: {pull_info}\n")
            self.refresh_repo_status()
            self.refresh_history()
        except Exception as e:
            error_message = f"Failed to pull changes: {str(e)}"
            self.update_status(error_message)
            self.remote_log.insert(tk.END, f"ERROR: {error_message}\n")
    
    def push_changes(self):
        if not self.repo:
            return
        
        try:
            # Check if remote exists
            if not self.repo.remotes:
                messagebox.showinfo("Info", "No remote repository configured. Please add a remote first.")
                return
            
            # Push changes
            push_info = self.repo.git.push('origin')
            self.update_status("Push completed successfully.")
            self.remote_log.insert(tk.END, f"Push completed: {push_info if push_info else 'Everything up-to-date'}\n")
        except Exception as e:
            error_message = f"Failed to push changes: {str(e)}"
            self.update_status(error_message)
            self.remote_log.insert(tk.END, f"ERROR: {error_message}\n")
    
    def update_status(self, message):
        self.status_var.set(message)


if __name__ == "__main__":
    root = tk.Tk()
    app = DawGitApp(root)
    root.mainloop()