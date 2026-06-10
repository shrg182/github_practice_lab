==== Tutorial Outline ====
 

[▶ chatgpt 2026-06-09 4:25 PM ](https://chatgpt.com/g/g-p-69d6676fff908191a75cba648ed0034f-visual-studio-code/c/6a0fa5be-bdc0-83ea-b4b6-1bdaced8cc95)

🧙🏾‍♂️ Below is a simple tutorial outline — a “directory” for how to compose this script step by step.

# Tutorial Outline: How to Build `create_chapter_dirs.py`

## 0. Goal of the script

Build a command-line Python script that can:

```text
1. Read a table-of-contents text file.
2. Detect chapter titles and section titles.
3. Convert those titles into safe folder names.
4. Create chapter folders.
5. Create section subfolders inside each chapter.
6. Optionally create README.md files from templates.
7. Support safe options such as --dry-run and --skip-readme.
```

---

# 1. Prepare the project structure

Before writing the script, prepare this folder structure:

```text
project_root/
├── chapters/
└── tools/
    └── utility_files/
        ├── create_chapter_dirs.py
        ├── python_toc.txt
        └── templates/
            ├── chapter_readme.md
            └── section_readme.md
```

The script lives here:

```text
tools/utility_files/create_chapter_dirs.py
```

The TOC input file lives here:

```text
tools/utility_files/python_toc.txt
```

The README templates live here:

```text
tools/utility_files/templates/
```

---

# 2. Write the script header

Start with:

```python
#!/usr/bin/env python3
```

Then add a docstring explaining:

```text
- script name
- purpose
- usage examples
```

Example:

```python
"""
create_chapter_dirs.py

Create chapter directories and subdirectories from a TOC text file.

Usage:
    python3 create_chapter_dirs.py
    python3 create_chapter_dirs.py --dry-run
    python3 create_chapter_dirs.py --skip-readme
"""
```

Purpose of this step:

> Make the script readable before the code begins.

---

# 3. Add imports

You need these modules:

```python
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
```

What each one does:

| Import      | Purpose                                   |
| ----------- | ----------------------------------------- |
| `argparse`  | command-line options                      |
| `re`        | regular expressions for parsing TOC lines |
| `dataclass` | simple class for chapter data             |
| `field`     | safe default empty list                   |
| `Path`      | modern file and folder paths              |
| `Template`  | fill README templates                     |

---

# 4. Define default paths

Next, define where the script should look for input and output.

```python
DEFAULT_TOC_FILE = Path(__file__).with_name("python_toc.txt")
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "chapters"
DEFAULT_TEMPLATE_DIR = Path(__file__).with_name("templates")
CHAPTER_README_TEMPLATE = DEFAULT_TEMPLATE_DIR / "chapter_readme.md"
SECTION_README_TEMPLATE = DEFAULT_TEMPLATE_DIR / "section_readme.md"
```

Purpose of this step:

> Let the script know where the TOC file, output folder, and template files are.

---

# 5. Create the `Chapter` data class

Create a simple object to store chapter information:

```python
@dataclass
class Chapter:
    """A chapter from the table of contents."""

    number: int
    title: str
    page: str
    sections: list[str] = field(default_factory=list)
```

Each chapter needs:

```text
chapter number
chapter title
starting page
section list
```

Example object:

```python
Chapter(
    number=1,
    title="Python Basics",
    page="1",
    sections=["Entering Expressions", "Variables"],
)
```

Purpose of this step:

> Store all information about one chapter in one organized object.

---

# 6. Write `parse_toc_line()`

This function should split one TOC line into:

```text
title
page number
```

Example input:

```text
Python Basics 7
```

Expected output:

```python
("Python Basics", "7")
```

Function:

```python
def parse_toc_line(line: str) -> tuple[str, str]:
    """Split a TOC line into title and page number."""
    match = re.match(
        r"^(.+?)\s+(\d+|[ivxlcdm]+)$",
        line.strip(),
        re.IGNORECASE,
    )

    if match is None:
        return line.strip(), ""

    return match.group(1).strip(), match.group(2)
```

Purpose of this step:

> Separate the readable title from the page number.

---

# 7. Write `load_chapters()`

This is one of the most important functions.

It should:

```text
1. Open the TOC text file.
2. Read it line by line.
3. Detect chapter lines.
4. Create Chapter objects.
5. Add section titles to the current chapter.
```

Main logic:

```python
current_chapter: Chapter | None = None
```

This means:

> At first, we are not inside any chapter yet.

When the script finds:

```text
Chapter 1: Python Basics 1
```

it creates a new `Chapter`.

When it later finds section lines, it adds them to:

```python
current_chapter.sections
```

Purpose of this step:

> Convert the text TOC file into structured Python data.

---

# 8. Write `slugify()`

This function converts titles into safe folder names.

Example:

```text
If-Else and Flow Control
```

becomes:

```text
if_else_and_flow_control
```

Function:

```python
def slugify(value: str) -> str:
    """Convert a title into a filesystem-friendly name."""
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return slug or "untitled"
```

Purpose of this step:

> Make sure folder names do not contain spaces, punctuation, or unsafe characters.

---

# 9. Write directory-name helper functions

## Chapter folder name

```python
def chapter_dir_name(chapter: Chapter) -> str:
    """Build the directory name for a chapter."""
    return f"chapter_{chapter.number:02d}_{slugify(chapter.title)}"
```

Example:

```text
chapter_01_python_basics
```

## Section folder name

```python
def section_dir_name(section_number: int, title: str) -> str:
    """Build the directory name for a chapter section."""
    return f"{section_number:02d}_{slugify(title)}"
```

Example:

```text
01_entering_expressions
```

Purpose of this step:

> Keep folder naming consistent across the whole project.

---

# 10. Write template-rendering function

This function reads a template file and fills placeholders.

```python
def render_template(template_path: Path, values: dict[str, str]) -> str:
    """Render a template file using named placeholders."""
    template = template_path.read_text(encoding="utf-8")
    return Template(template).safe_substitute(values)
```

A template might contain:

```md
# Chapter $chapter_number: $chapter_title

Starting page: $starting_page

## Sections

$section_list
```

Purpose of this step:

> Generate README text automatically instead of manually writing every README.

---

# 11. Write README text builders

## Chapter README builder

```python
def chapter_readme_text(chapter: Chapter) -> str:
    """Build README content for a chapter directory."""
    section_list = "\n".join(f"- [ ] {section}" for section in chapter.sections)

    if not section_list:
        section_list = "- [ ] Add study topics for this chapter."

    return render_template(
        CHAPTER_README_TEMPLATE,
        {
            "chapter_number": str(chapter.number),
            "chapter_title": chapter.title,
            "starting_page": chapter.page,
            "section_list": section_list,
        },
    )
```

Purpose:

> Create one README for a chapter folder.

## Section README builder

```python
def section_readme_text(chapter: Chapter, section_number: int, section: str) -> str:
    """Build README content for a section directory."""
    return render_template(
        SECTION_README_TEMPLATE,
        {
            "section_number": f"{section_number:02d}",
            "section_title": section,
            "chapter_number": str(chapter.number),
            "chapter_title": chapter.title,
        },
    )
```

Purpose:

> Create one README for each section folder.

---

# 12. Write file-writing function

```python
def write_readme(path: Path, content: str, overwrite: bool) -> bool:
    """Write a README file and return True if a file was created or updated."""
    readme_path = path / "README.md"

    if readme_path.exists() and not overwrite:
        return False

    readme_path.write_text(content, encoding="utf-8")
    return True
```

Important behavior:

```text
If README.md already exists and overwrite is False:
    skip it

If README.md does not exist:
    create it

If overwrite is True:
    replace it
```

Purpose of this step:

> Protect existing README files unless the user explicitly allows overwriting.

---

# 13. Write `create_directories()`

This function should create all chapter and section directories.

```python
def create_directories(
    chapters: list[Chapter],
    output_dir: Path,
    dry_run: bool = False,
) -> list[Path]:
    """Create chapter directories and section subdirectories."""
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
```

Purpose of this step:

> Actually create the folder tree.

---

# 14. Write `create_readmes()`

This function creates README files for all chapter and section folders.

```python
def create_readmes(
    chapters: list[Chapter],
    output_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False,
) -> list[Path]:
    """Create README files for chapter and section directories."""
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
```

Purpose of this step:

> Add useful starter documentation inside every generated folder.

---

# 15. Write the command-line parser

This lets the user run the script with options.

```python
def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Create chapter directories and section subdirectories from a TOC."
    )
```

Add options:

```python
parser.add_argument("--toc", type=Path, default=DEFAULT_TOC_FILE)
parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR)
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--skip-readme", action="store_true")
parser.add_argument("--overwrite-readme", action="store_true")
```

Purpose of this step:

> Make the script flexible from the terminal.

---

# 16. Write `main()`

The `main()` function connects everything.

It should:

```text
1. Parse command-line arguments.
2. Load chapters from the TOC file.
3. Create directories.
4. Optionally create README files.
5. Print a report.
6. Return 0 if successful.
```

Structure:

```python
def main() -> int:
    """Run the chapter directory creator."""
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
```

Purpose of this step:

> Run the script in the correct order.

---

# 17. Add the entry point

At the bottom:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

Purpose:

> Only run the script when executed directly.

This is better than:

```python
main()
```

because it returns a proper terminal exit code.

---

# 18. Implementation order

Write the script in this order:

```text
1. Header and docstring
2. Imports
3. Default path constants
4. Chapter dataclass
5. parse_toc_line()
6. load_chapters()
7. slugify()
8. chapter_dir_name()
9. section_dir_name()
10. render_template()
11. chapter_readme_text()
12. section_readme_text()
13. write_readme()
14. create_directories()
15. create_readmes()
16. build_parser()
17. main()
18. if __name__ == "__main__"
```

This order is practical because each later function depends on earlier functions.

---

# 19. Testing order

Test small parts first.

## Step 1: Test help

```bash
python3 tools/utility_files/create_chapter_dirs.py --help
```

## Step 2: Test TOC parsing without creating files

```bash
python3 tools/utility_files/create_chapter_dirs.py --dry-run
```

## Step 3: Test directory creation only

```bash
python3 tools/utility_files/create_chapter_dirs.py --dry-run --skip-readme
```

## Step 4: Actually create folders

```bash
python3 tools/utility_files/create_chapter_dirs.py --skip-readme
```

## Step 5: Create folders and README files

```bash
python3 tools/utility_files/create_chapter_dirs.py
```

## Step 6: Overwrite README files only when needed

```bash
python3 tools/utility_files/create_chapter_dirs.py --overwrite-readme
```

---

# 20. Mental model of the whole script

Think of the script as a pipeline:

```text
TOC text file
    ↓
parse lines
    ↓
Chapter objects
    ↓
safe folder names
    ↓
create folders
    ↓
render README templates
    ↓
write README files
    ↓
print report
```

Recommended next step: create the script skeleton first with only the imports, constants, `Chapter` class, and empty function names, then fill one function at a time.
