# Scripts

## todo_list.py

1. TXT

[▶︎ chatgpt previous version on 3e22 ](https://chatgpt.com/g/g-p-6762e6811cac8191866a6554d49273eb-tools/c/69da89d8-2f80-832b-a388-bc1a20f70336)


2. JSON

[► chatgpt 2026-06-03 6:03 PM ](https://chatgpt.com/g/g-p-6a18c2d2752c819185df514817e2367c-github-tutorial-project/c/6a2099a4-b910-83ea-946c-cca96b572dae)


```bash
python3 todo_list.py add "Study Python"
python3 todo_list.py add "Scrape TOC online from a PDF file"
python3 todo_list.py list
python3 todo_list.py done 1
python3 todo_list.py list
python3 todo_list.py delete 2
python3 todo_list.py list
```

## scrape

Python in Easy Steps

[▶︎ Source url ](https://ineasysteps.com/wp-content/uploads/2022/01/Python-in-easy-steps-2nd-edition-TOCCh1_Oct21reprint.pdf)

```bash
python3 -m pip install -r ../requirements.txt

python3 scrape_pdf_toc.py "https://ineasysteps.com/wp-content/uploads/2022/01/Python-in-easy-steps-2nd-edition-TOCCh1_Oct21reprint.pdf"

python3 scrape_pdf_toc.py "https://ineasysteps.com/wp-content/uploads/2022/01/Python-in-easy-steps-2nd-edition-TOCCh1_Oct21reprint.pdf" --output python_toc.txt

# Use this only if your Python install cannot verify the PDF site's SSL certificate.
python3 scrape_pdf_toc.py "https://ineasysteps.com/wp-content/uploads/2022/01/Python-in-easy-steps-2nd-edition-TOCCh1_Oct21reprint.pdf" --insecure

python3 scrape_pdf_toc.py "https://ineasysteps.com/wp-content/uploads/2022/01/Python-in-easy-steps-2nd-edition-TOCCh1_Oct21reprint.pdf" --insecure --output python_toc.txt
```

Chapter title rows are labeled in the output:

```text
Chapter 1: Getting started 7
Introducing Python 8
...
Chapter 2: Performing operations 25
```

What is this: (?)
python3 -m py_compile scripts/scrape_pdf_toc.py
python3 scripts/scrape_pdf_toc.py "..." --insecure --output scripts/python_toc.txt


## Create chapter directory: chapters

1. Create chapter directory for each chapter.
2. Create chapter subdirectories for the subtitles of each chapter.
3. Create a README.md study template in each chapter and subtitle directory.

```bash
python3 create_chapter_dirs.py --dry-run

python3 create_chapter_dirs.py

python3 create_chapter_dirs.py --skip-readme

python3 create_chapter_dirs.py --overwrite-readme
```

Example output structure:

```text
chapters/
  01_getting_started/
    README.md
    01_introducing_python/
      README.md
    02_installing_python_on_windows/
    03_installing_python_on_linux/
```


### README.md template

Create a separate template and use this template in create_chapter_dirs.py