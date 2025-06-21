#!/usr/bin/env python3
"""
A simple Python script example.
"""

import sys
import os


def main():
    """Main function."""
    print("Hello, world!")
    print(f"Python version: {sys.version}")
    
    # Example of various Python constructs
    data = {"name": "ftt", "version": "1.0.0"}
    
    for key, value in data.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main() 