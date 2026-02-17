# Siemens Documentation Converter

A Python utility to convert Siemens PDF documentation to Markdown format, preserving text structure and tables.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Convert a PDF (outputs to out/document.md by default)
python siemens_doc_converter.py document.pdf

# Save to custom path
python siemens_doc_converter.py document.pdf -o custom.md

# Convert specific pages (0-indexed)
python siemens_doc_converter.py document.pdf -p 0 1 2

# Extract images
python siemens_doc_converter.py document.pdf --images

# Batch convert a directory
python siemens_doc_converter.py pdfs --batch
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output path (default: `out/`) |
| `-p, --pages` | Page numbers to convert (0-indexed) |
| `--images` | Extract images from the PDF |
| `--image-dir` | Directory to save extracted images |
| `--batch` | Batch convert all PDFs in source directory |
| `-f, --force` | Overwrite existing output files (default: skip) |

## As a Module

```python
from siemens_doc_converter import convert_pdf_to_markdown

markdown = convert_pdf_to_markdown("document.pdf")

# Or save directly to file
convert_pdf_to_markdown("document.pdf", output_path="out/document.md")
```
