#!/usr/bin/env python3
"""
Practice 3: Display short help-style information.
"""


def main() -> None:
    print("Try these commands in the Python interpreter:")
    print("help(print)")
    print("help(str)")
    print("dir(str)")
    print()
    print("This script also shows one docstring:")
    print(str.upper.__doc__)


if __name__ == "__main__":
    main()
