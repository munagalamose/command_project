#!/usr/bin/env python3
"""
Demo script for Python Terminal
Shows various features and capabilities
"""

import os
import sys
from terminal import PythonTerminal


def run_demo():
    """Run a demonstration of the Python Terminal features."""
    print("Python Terminal Demo")
    print("=" * 50)
    print()
    
    # Create terminal instance
    terminal = PythonTerminal()
    
    # Demo commands
    demo_commands = [
        "help",
        "pwd",
        "ls",
        "mkdir demo_folder",
        "touch demo_file.txt",
        "ls",
        "echo 'Hello from Python Terminal!' > demo_file.txt",
        "cat demo_file.txt",
        "cpu",
        "memory",
        "whoami",
        "date",
        "ai 'create a file named ai_test.txt'",
        "ai 'show CPU usage'",
        "history",
        "rm demo_file.txt",
        "rm demo_folder",
        "ls"
    ]
    
    print("Running demo commands...")
    print("-" * 30)
    
    for i, command in enumerate(demo_commands, 1):
        print(f"\n[{i:2d}] {command}")
        print("-" * 40)
        
        try:
            output, success = terminal.execute_command(command)
            if output:
                print(output)
            if not success:
                print("Command failed or terminal exiting...")
                break
        except Exception as e:
            print(f"Error: {e}")
        
        # Small delay for readability
        import time
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("Demo completed!")


def interactive_demo():
    """Run an interactive demo session."""
    print("Interactive Python Terminal Demo")
    print("=" * 40)
    print("Try these commands:")
    print("- help")
    print("- ls")
    print("- ai 'create a file named test.txt'")
    print("- ai 'show CPU usage'")
    print("- history")
    print("- exit")
    print()
    
    terminal = PythonTerminal()
    terminal.run()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        run_demo()
