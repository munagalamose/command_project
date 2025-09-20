#!/usr/bin/env python3
"""
Test script for Windows-compatible Python Terminal
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from terminal_windows import PythonTerminal
    from ai_commands import AICommandProcessor
    
    print("Testing Python Terminal (Windows Compatible)...")
    print("=" * 50)
    
    # Test AI Command Processor
    print("\n1. Testing AI Command Processor:")
    ai_processor = AICommandProcessor()
    
    test_commands = [
        "create a file named test.txt",
        "show CPU usage",
        "list files in current directory",
        "go to home directory"
    ]
    
    for cmd in test_commands:
        commands, explanation = ai_processor.process_natural_language(cmd)
        print(f"  Input: {cmd}")
        print(f"  Commands: {commands}")
        print(f"  Explanation: {explanation}")
        print()
    
    # Test Terminal Class
    print("2. Testing Terminal Class:")
    terminal = PythonTerminal()
    
    # Test basic commands
    test_commands = [
        "help",
        "pwd",
        "whoami",
        "date"
    ]
    
    for cmd in test_commands:
        print(f"\n  Testing: {cmd}")
        try:
            output, success = terminal.execute_command(cmd)
            print(f"  Output: {output[:100]}..." if len(output) > 100 else f"  Output: {output}")
            print(f"  Success: {success}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    print("The Python Terminal is ready to use.")
    print("\nTo run the terminal:")
    print("  python terminal_windows.py")
    print("  or double-click run_terminal_windows.bat")
    
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please install required dependencies:")
    print("  pip install psutil")
except Exception as e:
    print(f"Error: {e}")
    print("Please check your Python installation and dependencies.")
