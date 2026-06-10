#!/usr/bin/env python3
"""
Practice 2: Use type() to inspect values.
"""


def main() -> None:
    values = [
        42,
        3.14,
        "Python",
        True,
        ["one", "two", "three"],
    ]

    for value in values:
        print(f"{value!r} is {type(value).__name__}")


if __name__ == "__main__":
    main()
