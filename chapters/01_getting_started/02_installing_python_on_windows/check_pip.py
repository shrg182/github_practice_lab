#!/usr/bin/env python3
"""
Practice 4: Check whether pip can be started from Python.
"""

from __future__ import annotations

import subprocess
import sys


def main() -> None:
    command = [sys.executable, "-m", "pip", "--version"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    if result.returncode == 0:
        print("pip is available.")
        print(result.stdout.strip())
    else:
        print("pip is not available from this Python executable.")
        print("Try installing Python again and choose the pip option.")


if __name__ == "__main__":
    main()
