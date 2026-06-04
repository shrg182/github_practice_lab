#!/usr/bin/env python3
"""
create_chapter_dirs.py

Create chapter directories and subdirectories from a TOC text file.

Usage:
    python3 create_chapter_dirs.py
    python3 create_chapter_dirs.py --toc python_toc.txt --output chapters
    python3 create_chapter_dirs.py --dry-run
    python3 create_chapter_dirs.py --skip-readme
    python3 create_chapter_dirs.py --help
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_TOC_FILE = Path(__file__).with_name("python_toc.txt")
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "chapters"


@dataclass
class Chapter:
    """
    A chapter from the table of contents.
    """

    number: int
    title: str
    page: str
    sections: list[str] = field(default_factory=list)


def parse_toc_line(line: str) -> tuple[str, str]:
    """
    Split a TOC line into title and page number.
    """
    match = re.match(r"^(.+?)\s+(\d+|[ivxlcdm]+)$", line.strip(), re.IGNORECASE)
    if match is None:
        return line.strip(), ""

    return match.group(1).strip(), match.group(2)


def load_chapters(toc_path: Path) -> list[Chapter]:
    """
    Load chapters and their section titles from a TOC file.
    """
    if not toc_path.exists():
        raise FileNotFoundError(f"TOC file not found: {toc_path}")

    chapters: list[Chapter] = []
    current_chapter: Chapter | None = None

    for raw_line in toc_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        chapter_match = re.match(r"^Chapter\s+(\d+):\s+(.+)$", line, re.IGNORECASE)
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
        if title.lower() == "index":
            continue

        current_chapter.sections.append(title)

    return chapters


def slugify(value: str) -> str:
    """
    Convert a title into a filesystem-friendly name.
    """
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return slug or "untitled"


def chapter_dir_name(chapter: Chapter) -> str:
    """
    Build the directory name for a chapter.
    """
    return f"{chapter.number:02d}_{slugify(chapter.title)}"


def section_dir_name(section_number: int, title: str) -> str:
    """
    Build the directory name for a chapter section.
    """
    return f"{section_number:02d}_{slugify(title)}"


def chapter_readme_text(chapter: Chapter) -> str:
    """
    Build README content for a chapter directory.
    """
    section_list = "\n".join(
        f"- [ ] {section}" for section in chapter.sections
    )
    if not section_list:
        section_list = "- [ ] Add study topics for this chapter."

    return f"""# Chapter {chapter.number}: {chapter.title}

Starting page: {chapter.page}

## Study Goals

- [ ] Read the chapter carefully.
- [ ] Understand the key Python ideas.
- [ ] Run the examples by hand.
- [ ] Explain the chapter in your own words.

## Sections

{section_list}

## Practice Plan

- [ ] Create small Python files for the examples.
- [ ] Modify each example at least once.
- [ ] Write notes about errors and fixes.
- [ ] Add one original practice exercise.

## Notes

Write important ideas, questions, and reminders here.
"""


def section_readme_text(chapter: Chapter, section_number: int, section: str) -> str:
    """
    Build README content for a section directory.
    """
    return f"""# {section_number:02d}. {section}

Chapter {chapter.number}: {chapter.title}

## Study Checklist

- [ ] Read this section.
- [ ] Type the example code yourself.
- [ ] Run the code and observe the output.
- [ ] Change the code and predict the result.
- [ ] Record one thing you learned.

## Practice

1. Recreate the section example.
2. Make one simple variation.
3. Write a short explanation of how it works.

## Notes

Add your notes, code snippets, and questions here.
"""


def write_readme(path: Path, content: str, overwrite: bool) -> bool:
    """
    Write a README file and return True if a file was created or updated.
    """
    readme_path = path / "README.md"
    if readme_path.exists() and not overwrite:
        return False

    readme_path.write_text(content, encoding="utf-8")
    return True


def create_readmes(
    chapters: list[Chapter],
    output_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False,
) -> list[Path]:
    """
    Create README files for chapter and section directories.
    """
    readme_paths = []

    for chapter in chapters:
        chapter_path = output_dir / chapter_dir_name(chapter)
        chapter_readme = chapter_path / "README.md"
        readme_paths.append(chapter_readme)

        if not dry_run:
            write_readme(chapter_path, chapter_readme_text(chapter), overwrite)

        for index, section in enumerate(chapter.sections, start=1):
            section_path = chapter_path / section_dir_name(index, section)
            section_readme = section_path / "README.md"
            readme_paths.append(section_readme)

            if not dry_run:
                write_readme(
                    section_path,
                    section_readme_text(chapter, index, section),
                    overwrite,
                )

    return readme_paths


def create_directories(
    chapters: list[Chapter],
    output_dir: Path,
    dry_run: bool = False,
) -> list[Path]:
    """
    Create chapter directories and section subdirectories.
    """
    paths = []

    for chapter in chapters:
        chapter_path = output_dir / chapter_dir_name(chapter)
        paths.append(chapter_path)

        for index, section in enumerate(chapter.sections, start=1):
            paths.append(chapter_path / section_dir_name(index, section))

    if not dry_run:
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)

    return paths


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Create chapter directories and section subdirectories from a TOC."
    )
    parser.add_argument(
        "--toc",
        type=Path,
        default=DEFAULT_TOC_FILE,
        help=f"Path to the TOC text file. Default: {DEFAULT_TOC_FILE}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory where chapter folders are created. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the directories that would be created without creating them.",
    )
    parser.add_argument(
        "--skip-readme",
        action="store_true",
        help="Create directories only, without README.md study files.",
    )
    parser.add_argument(
        "--overwrite-readme",
        action="store_true",
        help="Overwrite existing README.md files in chapter directories.",
    )
    return parser


def main() -> int:
    """
    Run the chapter directory creator.
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        chapters = load_chapters(args.toc)
    except FileNotFoundError as error:
        parser.error(str(error))

    if not chapters:
        parser.error("No chapters found. Expected lines like `Chapter 1: Title 7`.")

    paths = create_directories(chapters, args.output, dry_run=args.dry_run)
    readme_paths = []
    if not args.skip_readme:
        readme_paths = create_readmes(
            chapters,
            args.output,
            overwrite=args.overwrite_readme,
            dry_run=args.dry_run,
        )

    action = "Would create" if args.dry_run else "Created"
    print(f"{action} {len(paths)} directories:")
    for path in paths:
        print(path)

    if readme_paths:
        print(f"\n{action} {len(readme_paths)} README files:")
        for path in readme_paths:
            print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
