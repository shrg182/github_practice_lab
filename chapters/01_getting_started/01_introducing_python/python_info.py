#!/usr/bin/env python3
"""
Practice 2: Display basic information about the Python interpreter.
"""

from __future__ import annotations

import platform
import sys


def main() -> None:
    print(f"Python version: {platform.python_version()}")
    print(f"Python executable: {sys.executable}")
    print(f"Operating system: {platform.system()}")


if __name__ == "__main__":
    main()
