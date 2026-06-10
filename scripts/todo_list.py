#!/usr/bin/env python3
"""
todo_list.py

A simple command-line to-do list manager.

Features:
    - Add tasks
    - List tasks
    - Mark tasks as done
    - Delete tasks
    - Clear all tasks

Usage:
    python3 todo_list.py add "Study Python"
    python3 todo_list.py list
    python3 todo_list.py done 1
    python3 todo_list.py delete 1
    python3 todo_list.py clear
"""

from __future__ import annotations

import argparse
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

TODO_FILE = Path(__file__).with_name("todo_items.json")


def load_tasks() -> list[dict[str, Any]]:
    """
    Load tasks from the JSON file.

    Returns:
        A list of task dictionaries.
    """
    if not TODO_FILE.exists():
        return []

    try:
        with TODO_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except JSONDecodeError:
        print("Warning: todo_items.json is damaged or empty.")
        return []

    if not isinstance(tasks, list):
        print("Warning: todo_items.json does not contain a task list.")
        return []

    return tasks


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """
    Save tasks to the JSON file.

    Args:
        tasks: The list of task dictionaries to save.
    """
    with TODO_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def add_task(args: argparse.Namespace) -> None:
    """
    Add a new task.

    Args:
        args: Command-line arguments.
    """
    tasks = load_tasks()

    task = {
        "text": args.task,
        "done": False,
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Added task: {args.task}")


def list_tasks(args: argparse.Namespace) -> None:
    """
    Display all tasks.

    Args:
        args: Command-line arguments.
    """
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for index, task in enumerate(tasks, start=1):
        task_text = task.get("text", "Untitled task")
        task_done = task.get("done", False)

        status = "✓" if task_done else " "
        print(f"{index}. [{status}] {task_text}")


def mark_done(args: argparse.Namespace) -> None:
    """
    Mark a task as done.

    Args:
        args: Command-line arguments.
    """
    tasks = load_tasks()
    index = args.task_number - 1

    if index < 0 or index >= len(tasks):
        print("Invalid task number.")
        return

    tasks[index]["done"] = True
    save_tasks(tasks)

    print(f"Marked task {args.task_number} as done.")


def delete_task(args: argparse.Namespace) -> None:
    """
    Delete a task.

    Args:
        args: Command-line arguments.
    """
    tasks = load_tasks()
    index = args.task_number - 1

    if index < 0 or index >= len(tasks):
        print("Invalid task number.")
        return

    removed_task = tasks.pop(index)
    save_tasks(tasks)

    task_text = removed_task.get("text", "Untitled task")
    print(f"Deleted task: {task_text}")


def clear_tasks(args: argparse.Namespace) -> None:
    """
    Delete all tasks.

    Args:
        args: Command-line arguments.
    """
    save_tasks([])
    print("All tasks cleared.")


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.

    Returns:
        The configured ArgumentParser object.
    """
    parser = argparse.ArgumentParser(
        description="A simple command-line to-do list manager."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task.",
    )
    add_parser.add_argument(
        "task",
        help="The task description.",
    )
    add_parser.set_defaults(func=add_task)

    list_parser = subparsers.add_parser(
        "list",
        help="List all tasks.",
    )
    list_parser.set_defaults(func=list_tasks)

    done_parser = subparsers.add_parser(
        "done",
        help="Mark a task as done.",
    )
    done_parser.add_argument(
        "task_number",
        type=int,
        help="The task number to mark as done.",
    )
    done_parser.set_defaults(func=mark_done)

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task.",
    )
    delete_parser.add_argument(
        "task_number",
        type=int,
        help="The task number to delete.",
    )
    delete_parser.set_defaults(func=delete_task)

    clear_parser = subparsers.add_parser(
        "clear",
        help="Delete all tasks.",
    )
    clear_parser.set_defaults(func=clear_tasks)

    return parser


def main() -> None:
    """
    Run the to-do list program.
    """
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()