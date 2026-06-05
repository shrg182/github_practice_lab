#!/usr/bin/env python3
"""
scrape_pdf_toc.py

Download an online PDF file and extract likely table-of-contents entries.

Usage:
    python3 scrape_pdf_toc.py "https://example.com/book.pdf"
    python3 scrape_pdf_toc.py "https://example.com/book.pdf" --output toc.txt
"""

from __future__ import annotations

import argparse
import io
import re
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TOC_LINE_PATTERNS = [
    re.compile(r"^.+?\.{2,}\s*(?:\d+|[ivxlcdm]+)$", re.IGNORECASE),
    re.compile(r"^.+?\s{2,}(?:\d+|[ivxlcdm]+)$", re.IGNORECASE),
    re.compile(r"^[A-Za-z][A-Za-z0-9 ,:'&()/-]+?\s+(?:\d+|[ivxlcdm]+)$", re.IGNORECASE),
    re.compile(r"^(?:chapter\s+)?\d+\s+.+\s+(?:\d+|[ivxlcdm]+)$", re.IGNORECASE),
]


def download_pdf(url: str, verify_ssl: bool = True) -> bytes:
    """
    Download a PDF URL and return the file bytes.
    """
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; PDF TOC scraper)",
        },
    )

    context = None if verify_ssl else ssl._create_unverified_context()

    try:
        with urlopen(request, timeout=30, context=context) as response:
            content_type = response.headers.get("Content-Type", "")
            pdf_data = response.read()
    except HTTPError as error:
        raise RuntimeError(f"Download failed with HTTP {error.code}: {url}") from error
    except URLError as error:
        raise RuntimeError(f"Download failed: {error.reason}") from error

    if not pdf_data.startswith(b"%PDF") and "pdf" not in content_type.lower():
        raise RuntimeError("The URL did not look like a PDF file.")

    return pdf_data


def extract_page_text(pdf_data: bytes, max_pages: int) -> list[str]:
    """
    Extract text from the first pages of a PDF.
    """
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Missing dependency: install pypdf with `python3 -m pip install pypdf`."
        ) from error

    reader = PdfReader(io.BytesIO(pdf_data))
    page_count = min(max_pages, len(reader.pages))
    page_texts = []

    for page_number in range(page_count):
        page_text = reader.pages[page_number].extract_text() or ""
        page_texts.append(page_text)

    return page_texts


def clean_line(line: str) -> str:
    """
    Normalize whitespace in a PDF text line.
    """
    return re.sub(r"\s+", " ", line).strip()


def looks_like_toc_entry(line: str) -> bool:
    """
    Return True when a line resembles a TOC row.
    """
    if len(line) < 4:
        return False

    return any(pattern.match(line) for pattern in TOC_LINE_PATTERNS)


def extract_toc_lines(page_texts: list[str]) -> list[str]:
    """
    Extract likely table-of-contents lines from PDF page text.
    """
    all_lines = [
        clean_line(line)
        for page_text in page_texts
        for line in page_text.splitlines()
        if clean_line(line)
    ]

    contents_index = next(
        (
            index
            for index, line in enumerate(all_lines)
            if line.lower() in {"contents", "table of contents"}
        ),
        0,
    )

    toc_lines = []
    for line in all_lines[contents_index:]:
        if toc_lines and line.lower() in {"preface", "introduction", "chapter 1"}:
            break

        if looks_like_toc_entry(line):
            toc_lines.append(line)

    return remove_duplicates(toc_lines)


def remove_duplicates(lines: list[str]) -> list[str]:
    """
    Keep lines in order while removing exact duplicates.
    """
    seen = set()
    unique_lines = []

    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    return unique_lines


def get_entry_title(line: str) -> str:
    """
    Return the title part from a TOC line.
    """
    match = re.match(r"^(.+?)\s+(?:\d+|[ivxlcdm]+)$", line, re.IGNORECASE)
    if match is None:
        return line

    return match.group(1).strip()


def add_chapter_numbers(lines: list[str]) -> list[str]:
    """
    Prefix top-level chapter entries with their chapter numbers.
    """
    numbered_lines = []
    chapter_number = 0
    next_entry_is_chapter = True

    for line in lines:
        title = get_entry_title(line)

        if title.lower() == "index":
            numbered_lines.append(line)
            next_entry_is_chapter = False
            continue

        if next_entry_is_chapter:
            chapter_number += 1
            numbered_lines.append(f"Chapter {chapter_number}: {line}")
        else:
            numbered_lines.append(line)

        next_entry_is_chapter = title.lower() == "summary"

    return numbered_lines


def save_or_print(lines: list[str], output_path: Path | None) -> None:
    """
    Print TOC lines or save them to a text file.
    """
    toc_text = "\n".join(lines)

    if output_path is None:
        print(toc_text)
        return

    output_path.write_text(toc_text + "\n", encoding="utf-8")
    print(f"Saved {len(lines)} TOC entries to {output_path}")


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Scrape likely table-of-contents entries from an online PDF."
    )
    parser.add_argument(
        "url",
        help="The URL of the PDF file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional text file to save the extracted TOC.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=8,
        help="Number of PDF pages to scan from the start. Default: 8.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Skip SSL certificate verification for PDF sites with certificate issues.",
    )
    return parser


def main() -> int:
    """
    Run the PDF TOC scraper.
    """
    parser = build_parser()
    args = parser.parse_args()

    if args.max_pages < 1:
        parser.error("--max-pages must be at least 1.")

    try:
        pdf_data = download_pdf(args.url, verify_ssl=not args.insecure)
        page_texts = extract_page_text(pdf_data, args.max_pages)
        toc_lines = extract_toc_lines(page_texts)
        toc_lines = add_chapter_numbers(toc_lines)
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if not toc_lines:
        print("No TOC entries found.", file=sys.stderr)
        return 1

    save_or_print(toc_lines, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
