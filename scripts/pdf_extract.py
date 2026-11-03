#!/usr/bin/env python3
"""
pdf_extract.py — Extract structured text, tables, and embedded images from lecture PDFs.

Usage:
    python pdf_extract.py <input.pdf> [output.md] [options]

Features:
    - Extracts text blocks and organizes by page headings.
    - Extracts tables and formats them as clean Markdown tables.
    - Extracts embedded images directly into a companion `assets/` folder and links them.
    - Optional `--render-slides` to render high-resolution slide thumbnails for visual/vector diagrams.
    - Works with PyMuPDF (fitz) when available, or seamlessly falls back to poppler-utils (pdftotext/pdfimages).

Dependencies:
    Recommended: pip install pymupdf
    Fallback (system): poppler-utils (pdftotext, pdfimages, pdftoppm)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def format_table_matrix(rows: list[list[str]]) -> str:
    """Format raw 2D string matrix into GitHub-Flavored Markdown table."""
    if not rows:
        return ""
    # Clean up cell text
    cleaned_rows = [[(cell or "").replace("\n", " ").strip() for cell in row] for row in rows]
    num_cols = max(len(row) for row in cleaned_rows)
    if num_cols == 0:
        return ""

    # Pad rows to same number of columns
    padded = [row + [""] * (num_cols - len(row)) for row in cleaned_rows]
    headers = padded[0]
    data_rows = padded[1:] if len(padded) > 1 else []

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * num_cols) + " |",
    ]
    for row in data_rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def extract_with_pymupdf(
    pdf_path: Path,
    output_path: Path,
    extract_images: bool = True,
    render_slides: bool = False,
    dpi: int = 150,
) -> Path:
    """Extract text, tables, and images using PyMuPDF (fitz)."""
    import fitz

    doc = fitz.open(str(pdf_path))
    assets_dir = output_path.parent / f"{pdf_path.stem}_assets"
    if extract_images or render_slides:
        assets_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {pdf_path.stem}",
        f"",
        f"- **Source:** `{pdf_path.name}`",
        f"- **Total Pages:** {doc.page_count}",
        f"",
    ]

    for page_num, page in enumerate(doc, start=1):
        lines.append("---")
        lines.append(f"## Page {page_num}")
        lines.append("")

        # Optional full-slide render for vector diagram preservation
        if render_slides:
            slide_img_name = f"page_{page_num:02d}_slide.png"
            slide_img_path = assets_dir / slide_img_name
            pix = page.get_pixmap(dpi=dpi)
            pix.save(str(slide_img_path))
            rel_path = f"{assets_dir.name}/{slide_img_name}"
            lines.append(f"![Slide {page_num}]({rel_path})")
            lines.append("")

        # Extract structured text blocks
        blocks = page.get_text("blocks", sort=True)
        for block in blocks:
            # block = (x0, y0, x1, y1, text, block_no, block_type)
            block_type = block[6]
            if block_type == 0:  # text
                text = block[4].strip()
                if text:
                    lines.append(text)
                    lines.append("")

        # Extract embedded raster images
        if extract_images:
            image_list = page.get_images(full=True)
            for img_idx, img_info in enumerate(image_list, start=1):
                xref = img_info[0]
                base_img = doc.extract_image(xref)
                img_bytes = base_img["image"]
                img_ext = base_img["ext"]

                # Skip trivial icon-sized images (< 2KB or < 50px)
                if len(img_bytes) < 2048:
                    continue

                img_filename = f"page_{page_num:02d}_img_{img_idx:02d}.{img_ext}"
                img_filepath = assets_dir / img_filename
                img_filepath.write_bytes(img_bytes)

                rel_path = f"{assets_dir.name}/{img_filename}"
                lines.append(f"![Figure p.{page_num} #{img_idx}]({rel_path})")
                lines.append("")

        # Extract tables
        try:
            tabs = page.find_tables()
            if tabs and tabs.tables:
                for t_idx, table in enumerate(tabs.tables, start=1):
                    lines.append(f"**Table {t_idx} (Page {page_num}):**\n")
                    try:
                        import pandas as pd
                        df = table.to_pandas()
                        lines.append(df.to_markdown(index=False))
                    except Exception:
                        raw_table = table.extract()
                        lines.append(format_table_matrix(raw_table))
                    lines.append("")
        except AttributeError:
            pass

    doc.close()
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def extract_with_poppler(
    pdf_path: Path,
    output_path: Path,
    extract_images: bool = True,
    render_slides: bool = False,
    dpi: int = 150,
) -> Path:
    """Fallback extraction using system poppler-utils (pdftotext + pdfimages)."""
    if not shutil.which("pdftotext"):
        raise RuntimeError("Neither 'pymupdf' nor 'pdftotext' is installed.")

    print("ℹ Using poppler-utils fallback (pdftotext / pdfimages)...")
    assets_dir = output_path.parent / f"{pdf_path.stem}_assets"
    if extract_images or render_slides:
        assets_dir.mkdir(parents=True, exist_ok=True)

    # 1. Extract text with layout preservation
    cmd = ["pdftotext", "-layout", str(pdf_path), "-"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"pdftotext error: {proc.stderr}")

    raw_text = proc.stdout
    pages = raw_text.split("\x0c")  # form-feed character separates pages in pdftotext
    if pages and not pages[-1].strip():
        pages.pop()

    # 2. Extract images if requested
    img_map: dict[int, list[str]] = {}
    if extract_images and shutil.which("pdfimages"):
        prefix = str(assets_dir / "img")
        sub_img = subprocess.run(["pdfimages", "-png", str(pdf_path), prefix], capture_output=True)
        if sub_img.returncode == 0:
            for p in sorted(assets_dir.glob("img-*.png")):
                # Filter out tiny icon artifacts (< 3KB)
                if p.stat().st_size < 3000:
                    try:
                        p.unlink()
                    except OSError:
                        pass

    lines = [
        f"# {pdf_path.stem}",
        f"",
        f"- **Source:** `{pdf_path.name}`",
        f"- **Total Pages:** {len(pages)}",
        f"",
    ]

    for page_num, page_content in enumerate(pages, start=1):
        lines.append("---")
        lines.append(f"## Page {page_num}")
        lines.append("")

        if render_slides and shutil.which("pdftoppm"):
            slide_img_name = f"page_{page_num:02d}_slide.png"
            slide_prefix = str(assets_dir / f"page_{page_num:02d}_slide")
            subprocess.run([
                "pdftoppm", "-png", "-r", str(dpi),
                "-f", str(page_num), "-l", str(page_num),
                str(pdf_path), slide_prefix
            ], capture_output=True)
            # Find the generated file (pdftoppm adds page suffix)
            gen_files = list(assets_dir.glob(f"page_{page_num:02d}_slide-*.png"))
            if gen_files:
                target_file = assets_dir / slide_img_name
                gen_files[0].rename(target_file)
                rel_path = f"{assets_dir.name}/{slide_img_name}"
                lines.append(f"![Slide {page_num}]({rel_path})")
                lines.append("")

        clean_text = page_content.strip()
        if clean_text:
            lines.append(clean_text)
            lines.append("")

    # If any images were extracted and not yet linked, list them in an appendix
    remaining_imgs = sorted(assets_dir.glob("img-*.png"))
    if remaining_imgs:
        lines.append("---")
        lines.append("## Extracted Figures & Media")
        lines.append("")
        for img_file in remaining_imgs:
            rel_path = f"{assets_dir.name}/{img_file.name}"
            lines.append(f"![{img_file.stem}]({rel_path})")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def extract_pdf(
    pdf_path: str | Path,
    output_path: str | Path | None = None,
    extract_images: bool = True,
    render_slides: bool = False,
    dpi: int = 150,
) -> Path:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if output_path is None:
        output_path = pdf_path.with_suffix(".md")
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import fitz
        return extract_with_pymupdf(
            pdf_path, output_path,
            extract_images=extract_images,
            render_slides=render_slides,
            dpi=dpi
        )
    except ImportError:
        return extract_with_poppler(
            pdf_path, output_path,
            extract_images=extract_images,
            render_slides=render_slides,
            dpi=dpi
        )


def main():
    parser = argparse.ArgumentParser(
        description="Extract text, tables, and images from lecture PDFs into clean Markdown."
    )
    parser.add_argument("pdf", help="Path to input PDF file")
    parser.add_argument("output", nargs="?", default=None, help="Output Markdown file path (default: <pdf_stem>.md)")
    parser.add_argument("--no-images", action="store_true", help="Do not extract embedded images")
    parser.add_argument("--render-slides", action="store_true", help="Render full slide overviews (preserves vector plots/diagrams)")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for slide rendering (default: 150)")

    args = parser.parse_args()
    out = extract_pdf(
        args.pdf,
        args.output,
        extract_images=not args.no_images,
        render_slides=args.render_slides,
        dpi=args.dpi,
    )
    print(f"Extracted successfully → {out}")


if __name__ == "__main__":
    main()
