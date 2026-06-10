#!/usr/bin/env python3
"""
create_chapter_dirs.py

Create chapter directories and subdirectories from a TOC text file.

Usage:
    python3 create_chapter_dirs.py
    python3 create_chapter_dirs.py --dry-run
    python3 create_chapter_dirs.py --skip-readme
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from string import Template

DEFAULT_TOC_FILE = Path(__file__).with_name("python_toc.txt")
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "chapters"
DEFAULT_TEMPLATE_DIR = Path(__file__).with_name("templates")
CHAPTER_README_TEMPLATE = DEFAULT_TEMPLATE_DIR / "chapter_readme.md"
SECTION_README_TEMPLATE = DEFAULT_TEMPLATE_DIR / "section_readme.md"

@dataclass
class Chapter:
    """A chapter from the table of contents."""

    number: int
    title: str
    page: str
    sections: list[str] = field(default_factory=list)

