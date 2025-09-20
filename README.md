# Python Command Terminal

A fully functional command-line terminal built in Python that mimics real system terminal behavior with advanced features including AI-driven natural language command processing.

## Features

### Core Terminal Features
- **File & Directory Operations**: `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`, `cat`, `echo`, `touch`
- **System Monitoring**: CPU usage, memory usage, running processes, uptime, disk usage
- **Search & Text Processing**: `find`, `grep`, `head`, `tail`
- **Command History**: Persistent command history with auto-completion
- **Error Handling**: Comprehensive error handling with friendly messages

### AI-Powered Features
- **Natural Language Commands**: Convert natural language instructions into terminal commands
- **Smart Suggestions**: AI-driven command suggestions for unclear inputs
- **Intelligent Processing**: Context-aware command interpretation

### Advanced Features
- **Auto-completion**: Tab-completion for commands and file paths
- **Command History**: Persistent history across sessions
- **Cross-platform**: Works on Windows, macOS, and Linux
- **System Integration**: Direct system command execution
- **Responsive Interface**: Clean, fast, and user-friendly CLI

## Installation

1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage
```bash
python terminal_windows.py  # For Windows
python terminal.py          # For macOS/Linux
```

### Command Examples

#### File Operations
```bash
# List files
ls
ls /path/to/directory

# Change directory
cd /home/user
cd ..

# Create directory
mkdir new_folder

# Create file
touch new_file.txt

# Copy files
cp file1.txt file2.txt

# Move files
mv old_name.txt new_name.txt

# Remove files
rm unwanted_file.txt

# Read file contents
cat config.txt
```

#### System Monitoring
```bash
# CPU usage
cpu

# Memory usage
memory

# Running processes
ps

# System uptime
uptime

# Disk usage
df
```

#### AI Natural Language Commands
```bash
# Create files and folders
ai "create a file named test.txt"
ai "make a folder called projects"

# Navigate
ai "go to the home directory"
ai "where am I?"

# System monitoring
ai "show CPU usage"
ai "what's the memory usage?"

# Search operations
ai "find files named config"
ai "search for 'error' in log.txt"

# File operations
ai "copy file1.txt to backup/"
ai "read the file README.md"
```

#### Search and Text Processing
```bash
# Find files
find . -name "*.py"

# Search in files
grep "import" *.py

# Show first/last lines
head file.txt
tail file.txt -n 20
```

## Available Commands

### File & Directory Operations
- `ls [path]` - List files and directories
- `cd <path>` - Change directory
- `pwd` - Show current working directory
- `mkdir <name>` - Create directory
- `rm <path>` - Remove file or directory
- `cp <src> <dest>` - Copy file
- `mv <src> <dest>` - Move/rename file
- `cat <file>` - Display file contents
- `echo <text>` - Print text
- `touch <file>` - Create empty file

### System Monitoring
- `cpu` - Show CPU usage
- `memory` - Show memory usage
- `processes` - Show running processes
- `ps` - Alias for processes
- `uptime` - Show system uptime
- `df` - Show disk usage
- `du [path]` - Show directory size

### Search & Text
- `find <pattern>` - Find files
- `grep <pattern> <file>` - Search in file
- `head <file>` - Show first 10 lines
- `tail <file>` - Show last 10 lines

### Utilities
- `clear` - Clear screen
- `history` - Show command history
- `whoami` - Show current user
- `date` - Show current date/time
- `help` - Show help information
- `exit`/`quit` - Exit terminal

### AI Features
- `ai <command>` - Convert natural language to terminal commands

## AI Natural Language Examples

The AI system can understand and execute natural language commands:

### File Operations
- "create a file named test.txt" → `touch test.txt`
- "make a folder called projects" → `mkdir projects`
- "delete the file old.txt" → `rm old.txt`
- "list files in documents" → `ls documents`
- "read the file config.json" → `cat config.json`
- "copy file1.txt to backup/" → `cp file1.txt backup/`
- "move old.txt to trash/" → `mv old.txt trash/`

### Navigation
- "go to the home directory" → `cd ~`
- "navigate to documents" → `cd documents`
- "go up one level" → `cd ..`
- "where am I?" → `pwd`

### Search
- "find files named config" → `find . -name '*config*'`
- "search for 'error' in log.txt" → `grep "error" log.txt`

### System Monitoring
- "show CPU usage" → `cpu`
- "what's the memory usage?" → `memory`
- "list running processes" → `ps`
- "show system status" → `uptime`, `cpu`, `memory`

## Architecture

### Core Components

1. **PythonTerminal Class**: Main terminal engine
   - Command parsing and execution
   - File system operations
   - System monitoring
   - History management

2. **AICommandProcessor Class**: Natural language processing
   - Pattern matching for natural language
   - Command generation
   - Smart suggestions

3. **Command Categories**:
   - Built-in commands (ls, cd, etc.)
   - System commands (executed via subprocess)
   - AI commands (natural language processing)

### Key Features Implementation

- **Command History**: Persistent storage in `~/.python_terminal_history`
- **Auto-completion**: Using Python's `readline` module
- **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
- **Cross-platform**: OS detection and appropriate command execution
- **System Integration**: Direct subprocess execution for system commands

## Error Handling

The terminal provides comprehensive error handling:

- **File Operations**: Checks for file existence, permissions, and type
- **Directory Operations**: Validates paths and permissions
- **System Commands**: Handles timeouts and execution errors
- **AI Commands**: Graceful fallback for unrecognized patterns
- **User Input**: Handles invalid commands and malformed input

## Performance

- **Fast Startup**: Minimal initialization time
- **Efficient Commands**: Optimized file operations and system calls
- **Memory Management**: Efficient history storage and command processing
- **Responsive Interface**: Non-blocking command execution

## Extensibility

The terminal is designed for easy extension:

- **New Commands**: Add to the `execute_command` method
- **AI Patterns**: Extend the `command_patterns` dictionary
- **System Integration**: Add new system monitoring features
- **UI Enhancements**: Modify the prompt and output formatting

## Requirements

- Python 3.6+
- psutil (for system monitoring)
- pathlib2 (for Python < 3.4 compatibility)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Future Enhancements

- Web-based interface option
- Plugin system for custom commands
- Advanced AI features with machine learning
- Command scripting and automation
- Remote terminal capabilities
- Enhanced security features
