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


def parse_toc_line(line: str) -> tuple[str, str]:
    """Split a TOC line into title and page number."""
    cleaned_line = line.strip()

    cleaned_line = re.sub(r"\.{2,}", " ", cleaned_line)
    cleaned_line = re.sub(r"\s+", " ", cleaned_line)

    match = re.match(
        r"^(.+?)\s+(\d+|[ivxlcdm]+$)",
        cleaned_line,
        re.IGNORECASE
    )
    if match is None:
        return cleaned_line, ""
    
    title = match.group(1).strip()
    page = match.group(2).strip()

    return title, page


def load_chapter(toc_path: Path) -> list[Chapter]:
    """Load chapters and their section titles from a TOC file."""
    if not toc_path.is_file():
        raise FileNotFoundError(f"TOC file not found: {toc_path}")
    
    chapters: list[Chapter] = []
    current_chapter: Chapter | None = None

    chapter_pattern = re.compile(
        r"^Chapter\s(\d+):?\s+(.+)$",
        re.IGNORECASE
    )

    for raw_line in toc_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line:
            continue

        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            title, page = parse_toc_line(chapter_match.group(2))
            current_chapter = Chapter(
                number=int(chapter_match.group(1)),
                title=title,
                page=page,
            )
            chapters.append(current_chapter)
            continue

        if current_chapter is None:
            continue

        title, _page = parse_toc_line(line)

        if should_skip_toc_entry(title):
            continue

        current_chapter.sections.append(title)

    return chapters
 

def should_skip_toc_entry(entry: str) -> bool:
    """Return True for TOC entries that should be ignored."""
    normalized = re.sub(r"\s+", " ", entry.strip().lower())

    skipped_entries = {
        "contents",
        "preface",
        "introduction",
        "acknowledgments",
        "acknowledgements",
        "index",
        "table of contents",
        "appendix",
        "appendices",
        "about the author",
    }

    if normalized in skipped_entries:
        return True

    if re.fullmatch(r"chapter\s*\d+", normalized):
        return True

    if re.fullmatch(r"appendix\s*[a-zivxlcdm\d]+", normalized):
        return True

    return False


def slugify(value: str) -> str:
    """Convert a title into a filesystem-friendly name."""
    slug = value.lower()
    slog = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")

    return slug or "untitled"


def chapter_dir_name(chapter: Chapter) -> str:
    """Build the directory name for a chapter."""
    return f"chapter_{chapter.number:02d}_{slugify(chapter.title)}"


def section_dir_name(section_number: int, title: str) -> str:
    """Build the directory name for a chapter section."""
    return f"{section_number:02d}_slugify{title}"

