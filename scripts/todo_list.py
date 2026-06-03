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
from pathlib import Path
from typing import Any

TODO_FILE = Path("todo_items.json")


def load_tasks() -> list[dict[str, Any]]:
    """
    Load tasks from the JSON file.
    
    Returns:
        A list of task dictionaries.
    """
    if not TODO_FILE.exists():
        return []
    
    with TODO_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """
    Save tasks to the JSON file.

    Args:
        tasks: The list of task dictionaries to save.
    """
    with TODO_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def add_task(task_text: str) -> None:
    """
    Add a new task.
    
    Args:
        task_text: The task description.
    """
    tasks = load_tasks()

    task = {
        "text": task_text,
        "done": False
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Added task: {task_text}")


def list_tasks() -> None:
    """
    Display all tasks.
    """