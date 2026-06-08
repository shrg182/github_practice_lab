#!/usr/bin/env python3
"""
Practice 4: Simulate commands typed at the Python prompt.
"""


def show_prompt(command: str, result: object) -> None:
    print(f">>> {command}")
    print(result)


def main() -> None:
    name = "Python"

    show_prompt("name = 'Python'", "")
    show_prompt("name", name)
    show_prompt("name.lower()", name.lower())
    show_prompt("len(name)", len(name))
    show_prompt("'Py' in name", "Py" in name)


if __name__ == "__main__":
    main()
