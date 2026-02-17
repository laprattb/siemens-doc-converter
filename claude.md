# Siemens Documentation Converter

A Python utility that converts Siemens PDF documentation to Markdown format using `pymupdf4llm`, preserving text structure and tables.

## Project Structure

```
siemens-doc-converter/
├── siemens_doc_converter.py  # Main conversion script
├── postprocess.py            # Post-processing for TOC, headers, footers
├── requirements.txt          # Dependencies (pymupdf4llm)
├── pdfs/                     # Source PDFs (product documentation)
│   └── [subfolders]          # Organized by product/category
└── out/                      # Output markdown files (mirrors pdfs/ structure)
```

## Environment

Always use the virtual environment:
```bash
.venv/bin/python siemens_doc_converter.py [args]
```

## Usage

### Batch conversion (recommended)
```bash
# Convert all PDFs in pdfs/ to out/, preserving folder structure
.venv/bin/python siemens_doc_converter.py pdfs --batch

# With image extraction
.venv/bin/python siemens_doc_converter.py pdfs --batch --images

# Custom output directory
.venv/bin/python siemens_doc_converter.py pdfs -o custom_dir --batch
```

### Single file conversion
```bash
# Output to out/document.md (default)
.venv/bin/python siemens_doc_converter.py pdfs/document.pdf

# Save to custom path
.venv/bin/python siemens_doc_converter.py pdfs/document.pdf -o custom.md

# Convert specific pages (0-indexed)
.venv/bin/python siemens_doc_converter.py pdfs/document.pdf -p 0 1 2

# Extract images
.venv/bin/python siemens_doc_converter.py pdfs/document.pdf --images
```

### As a module
```python
from siemens_doc_converter import convert_pdf_to_markdown

markdown = convert_pdf_to_markdown("pdfs/document.pdf")
convert_pdf_to_markdown("pdfs/document.pdf", output_path="out/document.md")
```

## CLI Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output path (default: `out/`) |
| `-p, --pages` | Page numbers to convert (0-indexed, single file only) |
| `--images` | Extract images from the PDF |
| `--image-dir` | Directory to save extracted images (single file only) |
| `--batch` | Batch convert all PDFs in source directory |
| `-f, --force` | Overwrite existing output files (default: skip) |

## Workflow

PDFs in `pdfs/` are converted to Markdown in `out/`, preserving the folder structure:
- `pdfs/opint/manual.pdf` -> `out/opint/manual.md`
- `pdfs/umc/guide.pdf` -> `out/umc/guide.md`

## Dependencies

- `pymupdf4llm>=0.0.27` - PDF parsing and markdown conversion
