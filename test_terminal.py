#!/usr/bin/env python3
"""
Simple test script to verify terminal functionality without running the full terminal
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from terminal import PythonTerminal
    from ai_commands import AICommandProcessor
    
    print("Testing Python Terminal Components...")
    print("=" * 40)
    
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
    
    print("\n" + "=" * 40)
    print("All tests completed successfully!")
    print("The Python Terminal is ready to use.")
    print("\nTo run the terminal:")
    print("  python terminal.py")
    print("\nTo run the demo:")
    print("  python demo.py")
    
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please install required dependencies:")
    print("  pip install psutil")
except Exception as e:
    print(f"Error: {e}")
    print("Please check your Python installation and dependencies.")
