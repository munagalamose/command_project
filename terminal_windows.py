#!/usr/bin/env python3
"""
Python-Based Command Terminal - Windows Compatible Version
A fully functional command-line terminal that mimics real system terminal behavior.
"""

import os
import sys
import shutil
import subprocess
import platform
import psutil
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Callable
import glob
import argparse
from ai_commands import AICommandProcessor


class PythonTerminal:
    """Main terminal class that handles command processing and execution."""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.command_history = []
        self.history_file = os.path.join(os.path.expanduser("~"), ".python_terminal_history")
        self.ai_processor = AICommandProcessor()
        self.load_history()
        self.history_index = 0
        
    def get_available_commands(self) -> List[str]:
        """Get list of available commands for auto-completion."""
        return [
            'ls', 'cd', 'pwd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'echo', 'clear',
            'help', 'history', 'exit', 'quit', 'cpu', 'memory', 'processes', 'ps',
            'whoami', 'date', 'uptime', 'df', 'du', 'find', 'grep', 'head', 'tail',
            'ai', 'touch'
        ]
    
    def load_history(self):
        """Load command history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.command_history = f.read().splitlines()
        except Exception:
            self.command_history = []
    
    def save_history(self):
        """Save command history to file."""
        try:
            with open(self.history_file, 'w') as f:
                f.write('\n'.join(self.command_history))
        except Exception:
            pass
    
    def add_to_history(self, command: str):
        """Add command to history."""
        if command.strip() and (not self.command_history or self.command_history[-1] != command):
            self.command_history.append(command)
            if len(self.command_history) > 1000:  # Limit history size
                self.command_history = self.command_history[-1000:]
    
    def display_prompt(self):
        """Display the terminal prompt."""
        user = os.getenv('USERNAME', os.getenv('USER', 'user'))
        hostname = platform.node()
        current_path = os.path.basename(self.current_dir) or '/'
        return f"{user}@{hostname}:{current_path}$ "
    
    def get_user_input(self):
        """Get user input with basic history support."""
        try:
            command = input(self.display_prompt())
            return command
        except KeyboardInterrupt:
            return ""
        except EOFError:
            return "exit"
    
    def execute_command(self, command: str) -> Tuple[str, bool]:
        """
        Execute a command and return output and success status.
        
        Args:
            command: The command to execute
            
        Returns:
            Tuple of (output, success_status)
        """
        command = command.strip()
        if not command:
            return "", True
        
        # Add to history
        self.add_to_history(command)
        
        # Parse command
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        try:
            # Handle built-in commands
            if cmd in ['exit', 'quit']:
                return "Goodbye!", False
            
            elif cmd == 'help':
                return self.show_help(), True
            
            elif cmd == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                return "", True
            
            elif cmd == 'pwd':
                return self.current_dir, True
            
            elif cmd == 'ls':
                return self.list_directory(args), True
            
            elif cmd == 'cd':
                return self.change_directory(args), True
            
            elif cmd == 'mkdir':
                return self.create_directory(args), True
            
            elif cmd == 'rm':
                return self.remove_file_or_directory(args), True
            
            elif cmd == 'cp':
                return self.copy_file(args), True
            
            elif cmd == 'mv':
                return self.move_file(args), True
            
            elif cmd == 'cat':
                return self.cat_file(args), True
            
            elif cmd == 'echo':
                return self.echo_text(args), True
            
            elif cmd == 'history':
                return self.show_history(args), True
            
            elif cmd in ['cpu', 'memory', 'processes', 'ps']:
                return self.system_monitoring(cmd, args), True
            
            elif cmd == 'whoami':
                return os.getenv('USERNAME', os.getenv('USER', 'unknown')), True
            
            elif cmd == 'date':
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True
            
            elif cmd == 'uptime':
                return self.get_uptime(), True
            
            elif cmd == 'df':
                return self.get_disk_usage(), True
            
            elif cmd == 'du':
                return self.get_directory_size(args), True
            
            elif cmd == 'find':
                return self.find_files(args), True
            
            elif cmd == 'grep':
                return self.grep_text(args), True
            
            elif cmd == 'head':
                return self.head_file(args), True
            
            elif cmd == 'tail':
                return self.tail_file(args), True
            
            elif cmd == 'ai':
                return self.process_ai_command(args), True
            
            elif cmd == 'touch':
                return self.create_file(args), True
            
            else:
                # Try to execute as system command
                return self.execute_system_command(command), True
                
        except Exception as e:
            return f"Error: {str(e)}", False
    
    def show_help(self) -> str:
        """Display help information."""
        help_text = """
Python Terminal - Available Commands:

File & Directory Operations:
  ls [path]              List files and directories
  cd <path>              Change directory
  pwd                    Show current working directory
  mkdir <name>           Create directory
  rm <path>              Remove file or directory
  cp <src> <dest>        Copy file
  mv <src> <dest>        Move/rename file
  cat <file>             Display file contents
  echo <text>            Print text
  touch <file>           Create empty file

System Monitoring:
  cpu                    Show CPU usage
  memory                 Show memory usage
  processes              Show running processes
  ps                     Alias for processes
  uptime                 Show system uptime
  df                     Show disk usage
  du [path]              Show directory size

Search & Text:
  find <pattern>         Find files
  grep <pattern> <file>  Search in file
  head <file>            Show first 10 lines
  tail <file>            Show last 10 lines

Utilities:
  clear                  Clear screen
  history                Show command history
  whoami                 Show current user
  date                   Show current date/time
  help                   Show this help
  exit/quit              Exit terminal

AI Features:
  ai <command>           Convert natural language to terminal commands
        """
        return help_text.strip()
    
    def list_directory(self, args: List[str]) -> str:
        """List directory contents."""
        path = args[0] if args else self.current_dir
        try:
            if not os.path.exists(path):
                return f"ls: cannot access '{path}': No such file or directory"
            
            if not os.path.isdir(path):
                return f"ls: '{path}': Not a directory"
            
            items = os.listdir(path)
            if not items:
                return ""
            
            # Format output similar to ls -la
            output = []
            for item in sorted(items):
                item_path = os.path.join(path, item)
                try:
                    stat = os.stat(item_path)
                    size = stat.st_size
                    is_dir = os.path.isdir(item_path)
                    permissions = "drwxr-xr-x" if is_dir else "-rw-r--r--"
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%b %d %H:%M")
                    
                    if is_dir:
                        output.append(f"{permissions} {size:>8} {modified} {item}/")
                    else:
                        output.append(f"{permissions} {size:>8} {modified} {item}")
                except:
                    output.append(f"?????????? ????????? {item}")
            
            return "\n".join(output)
        except Exception as e:
            return f"ls: {str(e)}"
    
    def change_directory(self, args: List[str]) -> str:
        """Change current directory."""
        if not args:
            # Go to home directory
            new_dir = os.path.expanduser("~")
        else:
            path = args[0]
            if os.path.isabs(path):
                new_dir = path
            else:
                new_dir = os.path.join(self.current_dir, path)
        
        try:
            if not os.path.exists(new_dir):
                return f"cd: {new_dir}: No such file or directory"
            
            if not os.path.isdir(new_dir):
                return f"cd: {new_dir}: Not a directory"
            
            os.chdir(new_dir)
            self.current_dir = os.getcwd()
            return ""
        except Exception as e:
            return f"cd: {str(e)}"
    
    def create_directory(self, args: List[str]) -> str:
        """Create a new directory."""
        if not args:
            return "mkdir: missing operand"
        
        for dir_name in args:
            try:
                if os.path.isabs(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                else:
                    os.makedirs(os.path.join(self.current_dir, dir_name), exist_ok=True)
            except Exception as e:
                return f"mkdir: {str(e)}"
        
        return ""
    
    def remove_file_or_directory(self, args: List[str]) -> str:
        """Remove file or directory."""
        if not args:
            return "rm: missing operand"
        
        for path in args:
            try:
                if os.path.isabs(path):
                    target_path = path
                else:
                    target_path = os.path.join(self.current_dir, path)
                
                if not os.path.exists(target_path):
                    return f"rm: cannot remove '{path}': No such file or directory"
                
                if os.path.isdir(target_path):
                    shutil.rmtree(target_path)
                else:
                    os.remove(target_path)
            except Exception as e:
                return f"rm: {str(e)}"
        
        return ""
    
    def copy_file(self, args: List[str]) -> str:
        """Copy file or directory."""
        if len(args) < 2:
            return "cp: missing file operand"
        
        src = args[0]
        dest = args[1]
        
        try:
            if os.path.isabs(src):
                src_path = src
            else:
                src_path = os.path.join(self.current_dir, src)
            
            if os.path.isabs(dest):
                dest_path = dest
            else:
                dest_path = os.path.join(self.current_dir, dest)
            
            if not os.path.exists(src_path):
                return f"cp: cannot stat '{src}': No such file or directory"
            
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dest_path)
            
            return ""
        except Exception as e:
            return f"cp: {str(e)}"
    
    def move_file(self, args: List[str]) -> str:
        """Move or rename file or directory."""
        if len(args) < 2:
            return "mv: missing file operand"
        
        src = args[0]
        dest = args[1]
        
        try:
            if os.path.isabs(src):
                src_path = src
            else:
                src_path = os.path.join(self.current_dir, src)
            
            if os.path.isabs(dest):
                dest_path = dest
            else:
                dest_path = os.path.join(self.current_dir, dest)
            
            if not os.path.exists(src_path):
                return f"mv: cannot stat '{src}': No such file or directory"
            
            shutil.move(src_path, dest_path)
            return ""
        except Exception as e:
            return f"mv: {str(e)}"
    
    def cat_file(self, args: List[str]) -> str:
        """Display file contents."""
        if not args:
            return "cat: missing operand"
        
        output = []
        for file_path in args:
            try:
                if os.path.isabs(file_path):
                    full_path = file_path
                else:
                    full_path = os.path.join(self.current_dir, file_path)
                
                if not os.path.exists(full_path):
                    output.append(f"cat: {file_path}: No such file or directory")
                    continue
                
                if os.path.isdir(full_path):
                    output.append(f"cat: {file_path}: Is a directory")
                    continue
                
                with open(full_path, 'r', encoding='utf-8') as f:
                    output.append(f.read())
            except Exception as e:
                output.append(f"cat: {file_path}: {str(e)}")
        
        return "\n".join(output)
    
    def echo_text(self, args: List[str]) -> str:
        """Echo text to output."""
        return " ".join(args)
    
    def show_history(self, args: List[str]) -> str:
        """Show command history."""
        if not self.command_history:
            return "No commands in history"
        
        limit = 10
        if args and args[0].isdigit():
            limit = int(args[0])
        
        history_lines = []
        for i, cmd in enumerate(self.command_history[-limit:], 1):
            history_lines.append(f"{i:4d}  {cmd}")
        
        return "\n".join(history_lines)
    
    def system_monitoring(self, cmd: str, args: List[str]) -> str:
        """Handle system monitoring commands."""
        try:
            if cmd == 'cpu':
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                return f"CPU Usage: {cpu_percent}% (Cores: {cpu_count})"
            
            elif cmd == 'memory':
                memory = psutil.virtual_memory()
                return f"""Memory Usage:
Total: {memory.total // (1024**3)} GB
Available: {memory.available // (1024**3)} GB
Used: {memory.used // (1024**3)} GB ({memory.percent}%)
Free: {memory.free // (1024**3)} GB"""
            
            elif cmd in ['processes', 'ps']:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        proc_info = proc.info
                        processes.append(f"{proc_info['pid']:6d} {proc_info['name']:20s} {proc_info['cpu_percent']:6.1f}% {proc_info['memory_percent']:6.1f}%")
                    except:
                        continue
                
                header = "PID    NAME                 CPU%   MEM%"
                return f"{header}\n" + "\n".join(sorted(processes, key=lambda x: float(x.split()[2].rstrip('%')), reverse=True)[:20])
            
        except Exception as e:
            return f"Error getting system info: {str(e)}"
    
    def get_uptime(self) -> str:
        """Get system uptime."""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - boot_time
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"Uptime: {days} days, {hours} hours, {minutes} minutes"
        except:
            return "Uptime: Unable to determine"
    
    def get_disk_usage(self) -> str:
        """Get disk usage information."""
        try:
            disk_usage = psutil.disk_usage('/')
            total = disk_usage.total // (1024**3)
            used = disk_usage.used // (1024**3)
            free = disk_usage.free // (1024**3)
            percent = (used / total) * 100
            
            return f"""Disk Usage:
Total: {total} GB
Used: {used} GB ({percent:.1f}%)
Free: {free} GB"""
        except:
            return "Disk usage: Unable to determine"
    
    def get_directory_size(self, args: List[str]) -> str:
        """Get directory size."""
        path = args[0] if args else self.current_dir
        
        try:
            if os.path.isabs(path):
                target_path = path
            else:
                target_path = os.path.join(self.current_dir, path)
            
            if not os.path.exists(target_path):
                return f"du: '{path}': No such file or directory"
            
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(target_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
            
            size_mb = total_size / (1024**2)
            return f"{size_mb:.2f} MB\t{path}"
        except Exception as e:
            return f"du: {str(e)}"
    
    def find_files(self, args: List[str]) -> str:
        """Find files matching pattern."""
        if not args:
            return "find: missing search pattern"
        
        pattern = args[0]
        search_path = args[1] if len(args) > 1 else self.current_dir
        
        try:
            if os.path.isabs(search_path):
                target_path = search_path
            else:
                target_path = os.path.join(self.current_dir, search_path)
            
            if not os.path.exists(target_path):
                return f"find: '{search_path}': No such file or directory"
            
            matches = []
            for root, dirs, files in os.walk(target_path):
                for file in files:
                    if pattern in file:
                        matches.append(os.path.join(root, file))
            
            return "\n".join(matches) if matches else f"No files found matching '{pattern}'"
        except Exception as e:
            return f"find: {str(e)}"
    
    def grep_text(self, args: List[str]) -> str:
        """Search for text in files."""
        if len(args) < 2:
            return "grep: missing pattern or file"
        
        pattern = args[0]
        file_path = args[1]
        
        try:
            if os.path.isabs(file_path):
                full_path = file_path
            else:
                full_path = os.path.join(self.current_dir, file_path)
            
            if not os.path.exists(full_path):
                return f"grep: {file_path}: No such file or directory"
            
            if os.path.isdir(full_path):
                return f"grep: {file_path}: Is a directory"
            
            matches = []
            with open(full_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if pattern in line:
                        matches.append(f"{file_path}:{line_num}:{line.rstrip()}")
            
            return "\n".join(matches) if matches else f"No matches found for '{pattern}'"
        except Exception as e:
            return f"grep: {str(e)}"
    
    def head_file(self, args: List[str]) -> str:
        """Show first 10 lines of file."""
        if not args:
            return "head: missing file operand"
        
        file_path = args[0]
        lines = 10
        
        if len(args) > 1 and args[1].isdigit():
            lines = int(args[1])
        
        try:
            if os.path.isabs(file_path):
                full_path = file_path
            else:
                full_path = os.path.join(self.current_dir, file_path)
            
            if not os.path.exists(full_path):
                return f"head: {file_path}: No such file or directory"
            
            if os.path.isdir(full_path):
                return f"head: {file_path}: Is a directory"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                file_lines = f.readlines()
                return "".join(file_lines[:lines])
        except Exception as e:
            return f"head: {str(e)}"
    
    def tail_file(self, args: List[str]) -> str:
        """Show last 10 lines of file."""
        if not args:
            return "tail: missing file operand"
        
        file_path = args[0]
        lines = 10
        
        if len(args) > 1 and args[1].isdigit():
            lines = int(args[1])
        
        try:
            if os.path.isabs(file_path):
                full_path = file_path
            else:
                full_path = os.path.join(self.current_dir, file_path)
            
            if not os.path.exists(full_path):
                return f"tail: {file_path}: No such file or directory"
            
            if os.path.isdir(full_path):
                return f"tail: {file_path}: Is a directory"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                file_lines = f.readlines()
                return "".join(file_lines[-lines:])
        except Exception as e:
            return f"tail: {str(e)}"
    
    def process_ai_command(self, args: List[str]) -> str:
        """Process AI natural language commands."""
        if not args:
            return self.ai_processor.get_ai_help()
        
        natural_language = " ".join(args)
        commands, explanation = self.ai_processor.process_natural_language(natural_language)
        
        if not commands:
            return f"AI: {explanation}"
        
        output = [f"AI: {explanation}"]
        output.append("Executing commands:")
        
        for cmd in commands:
            output.append(f"  → {cmd}")
            cmd_output, success = self.execute_command(cmd)
            if cmd_output:
                output.append(cmd_output)
        
        return "\n".join(output)
    
    def create_file(self, args: List[str]) -> str:
        """Create an empty file."""
        if not args:
            return "touch: missing file operand"
        
        for filename in args:
            try:
                if os.path.isabs(filename):
                    file_path = filename
                else:
                    file_path = os.path.join(self.current_dir, filename)
                
                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Create empty file
                Path(file_path).touch()
            except Exception as e:
                return f"touch: {str(e)}"
        
        return ""
    
    def execute_system_command(self, command: str) -> str:
        """Execute system command using subprocess."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.current_dir
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\nError: {result.stderr}"
            
            return output if output else "Command executed successfully"
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def run(self):
        """Main terminal loop."""
        print("Python Terminal v1.0 (Windows Compatible)")
        print("Type 'help' for available commands or 'exit' to quit.")
        print("-" * 50)
        
        while True:
            try:
                # Get user input
                command = self.get_user_input()
                
                # Execute command
                output, continue_running = self.execute_command(command)
                
                # Display output
                if output:
                    print(output)
                
                # Exit if needed
                if not continue_running:
                    break
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit the terminal.")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
        
        # Save history before exiting
        self.save_history()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Python Command Terminal')
    parser.add_argument('--version', action='version', version='Python Terminal v1.0')
    args = parser.parse_args()
    
    terminal = PythonTerminal()
    terminal.run()


if __name__ == "__main__":
    main()
