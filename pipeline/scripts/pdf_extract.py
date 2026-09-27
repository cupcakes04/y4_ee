"""
pdf_extract.py — Stage 1: Extract text, tables, and image descriptions from lecture PDFs.

Usage:
    python pdf_extract.py <input.pdf> [output.txt]

If output path is omitted, writes to the same directory as the PDF with a .txt extension.

Dependencies:
    pip install pymupdf

Why pymupdf (fitz):
    - Handles scanned + digital PDFs
    - Extracts tables as structured blocks
    - Gives image bounding boxes so you can reference figure positions
    - Fast, no server needed
"""

import sys
import fitz  # pymupdf
from pathlib import Path


def extract_pdf(pdf_path: str, output_path: str | None = None) -> Path:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if output_path is None:
        output_path = pdf_path.with_suffix(".txt")
    else:
        output_path = Path(output_path)

    doc = fitz.open(str(pdf_path))
    lines = []

    lines.append(f"# Extracted: {pdf_path.name}")
    lines.append(f"# Pages: {doc.page_count}")
    lines.append("")

    for page_num, page in enumerate(doc, start=1):
        lines.append(f"---")
        lines.append(f"## Page {page_num}")
        lines.append("")

        # --- Text blocks ---
        blocks = page.get_text("blocks", sort=True)
        for block in blocks:
            # block = (x0, y0, x1, y1, text, block_no, block_type)
            block_type = block[6]
            if block_type == 0:  # text block
                text = block[4].strip()
                if text:
                    lines.append(text)
                    lines.append("")
            elif block_type == 1:  # image block
                bbox = block[:4]
                lines.append(f"[IMAGE at page {page_num}, bbox {tuple(round(b) for b in bbox)}]")
                lines.append("  → Describe what this figure shows manually, or re-upload to Gemini.")
                lines.append("")

        # --- Tables (heuristic: look for structured text regions) ---
        # pymupdf 1.23+ has find_tables()
        try:
            tables = page.find_tables()
            if tables.tables:
                for t_idx, table in enumerate(tables.tables, start=1):
                    lines.append(f"[TABLE {t_idx} on page {page_num}]")
                    df = table.to_pandas()
                    # markdown table
                    lines.append(df.to_markdown(index=False))
                    lines.append("")
        except AttributeError:
            # older pymupdf — skip table extraction, note it
            pass

    doc.close()

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Extracted → {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_extract.py <input.pdf> [output.txt]")
        sys.exit(1)

    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    extract_pdf(pdf, out)
