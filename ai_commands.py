#!/usr/bin/env python3
"""
AI-driven Natural Language Command Processing
Converts natural language instructions into terminal commands.
"""

import re
import os
from typing import List, Dict, Tuple, Optional, Callable


class AICommandProcessor:
    """Processes natural language commands and converts them to terminal commands."""
    
    def __init__(self):
        self.command_patterns = {
            # File operations
            'create_file': [
                r'create\s+(?:a\s+)?file\s+(?:named\s+)?([^\s]+)',
                r'make\s+(?:a\s+)?file\s+(?:named\s+)?([^\s]+)',
                r'new\s+file\s+(?:named\s+)?([^\s]+)'
            ],
            'create_folder': [
                r'create\s+(?:a\s+)?(?:folder|directory)\s+(?:named\s+)?([^\s]+)',
                r'make\s+(?:a\s+)?(?:folder|directory)\s+(?:named\s+)?([^\s]+)',
                r'new\s+(?:folder|directory)\s+(?:named\s+)?([^\s]+)',
                r'mkdir\s+([^\s]+)'
            ],
            'delete_file': [
                r'delete\s+(?:the\s+)?(?:file\s+)?([^\s]+)',
                r'remove\s+(?:the\s+)?(?:file\s+)?([^\s]+)',
                r'rm\s+([^\s]+)'
            ],
            'delete_folder': [
                r'delete\s+(?:the\s+)?(?:folder|directory)\s+([^\s]+)',
                r'remove\s+(?:the\s+)?(?:folder|directory)\s+([^\s]+)',
                r'rmdir\s+([^\s]+)'
            ],
            'list_files': [
                r'list\s+(?:files\s+)?(?:in\s+)?([^\s]*)',
                r'show\s+(?:files\s+)?(?:in\s+)?([^\s]*)',
                r'ls\s*([^\s]*)'
            ],
            'change_directory': [
                r'go\s+to\s+([^\s]+)',
                r'navigate\s+to\s+([^\s]+)',
                r'enter\s+([^\s]+)',
                r'cd\s+([^\s]+)'
            ],
            'copy_file': [
                r'copy\s+([^\s]+)\s+to\s+([^\s]+)',
                r'cp\s+([^\s]+)\s+([^\s]+)'
            ],
            'move_file': [
                r'move\s+([^\s]+)\s+to\s+([^\s]+)',
                r'mv\s+([^\s]+)\s+([^\s]+)'
            ],
            'read_file': [
                r'read\s+(?:the\s+)?(?:file\s+)?([^\s]+)',
                r'show\s+(?:the\s+)?(?:contents\s+of\s+)?([^\s]+)',
                r'cat\s+([^\s]+)'
            ],
            'search_files': [
                r'find\s+(?:files\s+)?(?:named\s+)?([^\s]+)',
                r'search\s+for\s+([^\s]+)',
                r'locate\s+([^\s]+)'
            ],
            'search_text': [
                r'search\s+for\s+"([^"]+)"\s+in\s+([^\s]+)',
                r'grep\s+"([^"]+)"\s+([^\s]+)',
                r'find\s+"([^"]+)"\s+in\s+([^\s]+)'
            ],
            
            # System monitoring
            'cpu_usage': [
                r'show\s+cpu\s+usage',
                r'what\s+is\s+the\s+cpu\s+usage',
                r'cpu\s+status',
                r'cpu'
            ],
            'memory_usage': [
                r'show\s+memory\s+usage',
                r'what\s+is\s+the\s+memory\s+usage',
                r'memory\s+status',
                r'memory'
            ],
            'running_processes': [
                r'show\s+running\s+processes',
                r'list\s+processes',
                r'what\s+processes\s+are\s+running',
                r'ps'
            ],
            'system_info': [
                r'show\s+system\s+info',
                r'system\s+status',
                r'uptime'
            ],
            
            # Navigation
            'current_directory': [
                r'where\s+am\s+i',
                r'current\s+directory',
                r'pwd'
            ],
            'go_home': [
                r'go\s+home',
                r'navigate\s+home',
                r'cd\s+~'
            ],
            'go_up': [
                r'go\s+up',
                r'go\s+back',
                r'cd\s+\.\.'
            ],
            
            # Help
            'help': [
                r'help',
                r'what\s+commands\s+are\s+available',
                r'show\s+help'
            ],
            'clear_screen': [
                r'clear\s+screen',
                r'clear',
                r'cls'
            ]
        }
    
    def process_natural_language(self, text: str) -> Tuple[List[str], str]:
        """
        Process natural language input and return terminal commands.
        
        Args:
            text: Natural language input
            
        Returns:
            Tuple of (commands, explanation)
        """
        text = text.strip().lower()
        commands = []
        explanation = ""
        
        # Check each command pattern
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    commands, explanation = self._generate_commands(command_type, match, text)
                    if commands:
                        return commands, explanation
        
        # If no pattern matches, try to extract file/folder names and suggest commands
        return self._suggest_commands(text)
    
    def _generate_commands(self, command_type: str, match: re.Match, original_text: str) -> Tuple[List[str], str]:
        """Generate commands based on matched pattern."""
        groups = match.groups()
        
        if command_type == 'create_file':
            filename = groups[0]
            commands = [f"touch {filename}"]
            explanation = f"Creating file '{filename}'"
            
        elif command_type == 'create_folder':
            foldername = groups[0]
            commands = [f"mkdir {foldername}"]
            explanation = f"Creating directory '{foldername}'"
            
        elif command_type == 'delete_file':
            filename = groups[0]
            commands = [f"rm {filename}"]
            explanation = f"Deleting file '{filename}'"
            
        elif command_type == 'delete_folder':
            foldername = groups[0]
            commands = [f"rm -r {foldername}"]
            explanation = f"Deleting directory '{foldername}'"
            
        elif command_type == 'list_files':
            path = groups[0] if groups[0] else ""
            commands = [f"ls {path}"]
            explanation = f"Listing files in '{path}'" if path else "Listing files in current directory"
            
        elif command_type == 'change_directory':
            path = groups[0]
            commands = [f"cd {path}"]
            explanation = f"Changing to directory '{path}'"
            
        elif command_type == 'copy_file':
            src, dest = groups
            commands = [f"cp {src} {dest}"]
            explanation = f"Copying '{src}' to '{dest}'"
            
        elif command_type == 'move_file':
            src, dest = groups
            commands = [f"mv {src} {dest}"]
            explanation = f"Moving '{src}' to '{dest}'"
            
        elif command_type == 'read_file':
            filename = groups[0]
            commands = [f"cat {filename}"]
            explanation = f"Reading file '{filename}'"
            
        elif command_type == 'search_files':
            pattern = groups[0]
            commands = [f"find . -name '*{pattern}*'"]
            explanation = f"Searching for files matching '{pattern}'"
            
        elif command_type == 'search_text':
            text, filename = groups
            commands = [f'grep "{text}" {filename}']
            explanation = f"Searching for '{text}' in '{filename}'"
            
        elif command_type == 'cpu_usage':
            commands = ["cpu"]
            explanation = "Showing CPU usage"
            
        elif command_type == 'memory_usage':
            commands = ["memory"]
            explanation = "Showing memory usage"
            
        elif command_type == 'running_processes':
            commands = ["ps"]
            explanation = "Showing running processes"
            
        elif command_type == 'system_info':
            commands = ["uptime", "cpu", "memory"]
            explanation = "Showing system information"
            
        elif command_type == 'current_directory':
            commands = ["pwd"]
            explanation = "Showing current directory"
            
        elif command_type == 'go_home':
            commands = ["cd ~"]
            explanation = "Going to home directory"
            
        elif command_type == 'go_up':
            commands = ["cd .."]
            explanation = "Going up one directory"
            
        elif command_type == 'help':
            commands = ["help"]
            explanation = "Showing help information"
            
        elif command_type == 'clear_screen':
            commands = ["clear"]
            explanation = "Clearing screen"
            
        else:
            return [], ""
        
        return commands, explanation
    
    def _suggest_commands(self, text: str) -> Tuple[List[str], str]:
        """Suggest commands based on keywords in the text."""
        suggestions = []
        explanation = "I couldn't understand that command. Here are some suggestions:"
        
        # Extract potential file/folder names
        words = text.split()
        potential_names = [word for word in words if '.' in word or word.isalnum()]
        
        if 'file' in text or 'document' in text:
            if potential_names:
                suggestions.append(f"cat {potential_names[0]}")
                suggestions.append(f"ls {potential_names[0]}")
            else:
                suggestions.append("ls")
                suggestions.append("cat <filename>")
        
        if 'folder' in text or 'directory' in text:
            if potential_names:
                suggestions.append(f"mkdir {potential_names[0]}")
                suggestions.append(f"cd {potential_names[0]}")
            else:
                suggestions.append("ls")
                suggestions.append("mkdir <foldername>")
        
        if 'search' in text or 'find' in text:
            suggestions.append("find . -name '*pattern*'")
            suggestions.append("grep 'text' filename")
        
        if 'system' in text or 'status' in text:
            suggestions.extend(["cpu", "memory", "ps", "uptime"])
        
        if not suggestions:
            suggestions = ["help", "ls", "pwd", "cpu", "memory"]
        
        return suggestions, explanation
    
    def get_ai_help(self) -> str:
        """Get help for AI commands."""
        return """
AI Natural Language Commands:

File Operations:
  "create a file named test.txt"     → touch test.txt
  "make a folder called projects"    → mkdir projects
  "delete the file old.txt"          → rm old.txt
  "list files in documents"          → ls documents
  "read the file config.json"        → cat config.json
  "copy file1.txt to backup/"        → cp file1.txt backup/
  "move old.txt to trash/"           → mv old.txt trash/

Navigation:
  "go to the home directory"         → cd ~
  "navigate to documents"            → cd documents
  "go up one level"                  → cd ..
  "where am I?"                     → pwd

Search:
  "find files named config"          → find . -name '*config*'
  "search for 'error' in log.txt"    → grep "error" log.txt

System Monitoring:
  "show CPU usage"                   → cpu
  "what's the memory usage?"         → memory
  "list running processes"           → ps
  "show system status"               → uptime, cpu, memory

Utilities:
  "clear the screen"                 → clear
  "show help"                        → help

Usage: Type 'ai <your natural language command>' to use AI features.
        """
    
    def is_ai_command(self, text: str) -> bool:
        """Check if the text is an AI command."""
        return text.strip().lower().startswith('ai ')
    
    def extract_ai_command(self, text: str) -> str:
        """Extract the natural language part from 'ai <command>'."""
        return text[3:].strip()


def main():
    """Test the AI command processor."""
    processor = AICommandProcessor()
    
    test_commands = [
        "create a file named test.txt",
        "make a folder called projects",
        "list files in the current directory",
        "show CPU usage",
        "go to the home directory",
        "search for files named config",
        "read the file README.md"
    ]
    
    print("AI Command Processor Test")
    print("=" * 40)
    
    for cmd in test_commands:
        print(f"\nInput: {cmd}")
        commands, explanation = processor.process_natural_language(cmd)
        print(f"Commands: {commands}")
        print(f"Explanation: {explanation}")


if __name__ == "__main__":
    main()
