#!/usr/bin/env python3
"""
pdf_to_txt.py — Batch-convert all PDFs in a folder to plain .txt files.

Usage:
    python batch_pdf_to_txt.py <input_folder> <output_folder>

Example with uv:
    uv run batch_pdf_to_txt.py ./data/downloads ./data/txt_downloads
    python batch_pdf_to_txt.py ./data/downloads ./data/txt_downloads
"""

import sys
from pathlib import Path
import fitz  # PyMuPDF


def extract_text(pdf_path: Path) -> str:
    """Extract all text from a PDF file using PyMuPDF."""
    doc = fitz.open(str(pdf_path))
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text() or ""
        if text.strip():
            pages.append(f"--- Page {i} ---\n{text.strip()}")
    doc.close()
    return "\n\n".join(pages)


def convert_folder(input_folder: str, output_folder: str) -> None:
    in_path = Path(input_folder)
    out_path = Path(output_folder)

    if not in_path.is_dir():
        print(f"Error: '{input_folder}' is not a valid directory.")
        sys.exit(1)

    out_path.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(in_path.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{input_folder}'.")
        return

    print(f"Found {len(pdf_files)} PDF(s) in '{input_folder}'.\n")

    success, failed = 0, 0
    for pdf_file in pdf_files:
        txt_name = pdf_file.stem + ".txt"
        txt_path = out_path / txt_name
        try:
            text = extract_text(pdf_file)
            txt_path.write_text(text, encoding="utf-8")
            print(f"  ✓ {pdf_file.name}  →  {txt_name}")
            success += 1
        except Exception as e:
            print(f"  ✗ {pdf_file.name}  — {e}")
            failed += 1

    print(f"\nDone: {success} converted, {failed} failed.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip())
        sys.exit(1)
    convert_folder(sys.argv[1], sys.argv[2])