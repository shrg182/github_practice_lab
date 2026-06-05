#!/usr/bin/env python3
"""
Practice 2: Show where Python is installed.
"""

from __future__ import annotations

import sys


def main() -> None:
    print(f"Python executable path: {sys.executable}")
    print()
    print("On Windows, this path often includes one of these folders:")
    print("C:\\Users\\YourName\\AppData\\Local\\Programs\\Python")
    print("C:\\Program Files\\Python")


if __name__ == "__main__":
    main()
