#!/usr/bin/env python3
"""
Practice 1: Check the Python version.
"""

from __future__ import annotations

import platform


def main() -> None:
    version = platform.python_version()

    print(f"Python version: {version}")
    print("On Windows, compare this with the version shown by:")
    print("py --version")
    print("python --version")


if __name__ == "__main__":
    main()
