#!/usr/bin/env python3
"""
Practice 3: Check whether Python commands are available on PATH.
"""

from __future__ import annotations

from shutil import which


def main() -> None:
    commands = ["python", "python3", "py", "pip", "pip3"]

    for command in commands:
        location = which(command)
        if location is None:
            print(f"{command}: not found")
        else:
            print(f"{command}: {location}")

    print()
    print("On Windows, `py` is the Python launcher and is often the best command to try.")


if __name__ == "__main__":
    main()
