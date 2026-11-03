#!/usr/bin/env python3
"""
pdf_crop.py — Visual diagram, equation, and figure cropper for lecture PDFs & images.

Extract high-resolution, crisp crops of schematics, Bode plots, block diagrams,
circuits, and equations to embed directly into Markdown concept notes.

Usage:
    python pdf_crop.py <input.pdf> -p <page> [options]
    python pdf_crop.py <input.png/jpg> [options]

Examples:
    # 1. Render full slide 5 at 300 DPI:
    python pdf_crop.py lecture.pdf -p 5 --full-page -o assets/slide5.png

    # 2. Crop top-half or bottom-half using presets:
    python pdf_crop.py lecture.pdf -p 3 --preset bottom-half -o assets/bode_plot.png

    # 3. Crop by normalized bounding box (left, top, right, bottom in 0.0-1.0):
    python pdf_crop.py lecture.pdf -p 4 --bbox 0.1,0.25,0.9,0.75 -o assets/circuit.png

    # 4. Crop an existing image:
    python pdf_crop.py screenshot.png --bbox 100,50,600,400 -o assets/cropped.png
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image

# Preset bounding boxes as normalized fractions: (left, top, right, bottom)
PRESETS = {
    "top-half": (0.0, 0.0, 1.0, 0.52),
    "bottom-half": (0.0, 0.48, 1.0, 1.0),
    "left-half": (0.0, 0.0, 0.52, 1.0),
    "right-half": (0.48, 0.0, 1.0, 1.0),
    "top-left": (0.0, 0.0, 0.52, 0.52),
    "top-right": (0.48, 0.0, 1.0, 0.52),
    "bottom-left": (0.0, 0.48, 0.52, 1.0),
    "bottom-right": (0.48, 0.48, 1.0, 1.0),
    "center": (0.15, 0.15, 0.85, 0.85),
    "slide-body": (0.05, 0.12, 0.95, 0.92),  # Excludes slide title and footer
}


def parse_bbox_string(bbox_str: str) -> tuple[float, float, float, float]:
    """Parse comma or space separated bounding box."""
    clean = bbox_str.replace(" ", ",").replace(";", ",")
    parts = [float(p.strip()) for p in clean.split(",") if p.strip()]
    if len(parts) != 4:
        raise ValueError(f"Expected 4 values (x0, y0, x1, y1), got: {bbox_str}")
    return tuple(parts)


def render_pdf_page_pymupdf(pdf_path: Path, page_num: int, dpi: int) -> Image.Image:
    """Render a PDF page to PIL Image using PyMuPDF (fitz)."""
    import fitz
    doc = fitz.open(str(pdf_path))
    if page_num < 1 or page_num > len(doc):
        raise ValueError(f"Page {page_num} out of range (1..{len(doc)})")
    page = doc[page_num - 1]
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img


def render_pdf_page_poppler(pdf_path: Path, page_num: int, dpi: int) -> Image.Image:
    """Render a PDF page to PIL Image using pdftoppm (poppler-utils)."""
    if not shutil.which("pdftoppm"):
        raise RuntimeError("Neither 'pymupdf' nor 'pdftoppm' is available to render PDFs.")
    
    cmd = [
        "pdftoppm",
        "-png",
        "-r", str(dpi),
        "-f", str(page_num),
        "-l", str(page_num),
        str(pdf_path),
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        raise RuntimeError(f"pdftoppm failed on page {page_num}: {res.stderr.decode()}")
    
    # pdftoppm outputs image directly to stdout if no prefix, or prefix-N.png
    # Let's run with prefix in a temp location
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = os.path.join(tmpdir, "render")
        cmd_temp = [
            "pdftoppm",
            "-png",
            "-r", str(dpi),
            "-f", str(page_num),
            "-l", str(page_num),
            str(pdf_path),
            prefix
        ]
        sub = subprocess.run(cmd_temp, capture_output=True)
        if sub.returncode != 0:
            raise RuntimeError(f"pdftoppm render failed: {sub.stderr.decode()}")
        files = list(Path(tmpdir).glob("*.png"))
        if not files:
            raise RuntimeError("pdftoppm did not produce an image.")
        img = Image.open(files[0]).copy()
        return img


def render_pdf_page(pdf_path: Path, page_num: int, dpi: int) -> Image.Image:
    """Render PDF page trying pymupdf first, falling back to pdftoppm."""
    try:
        return render_pdf_page_pymupdf(pdf_path, page_num, dpi)
    except ImportError:
        return render_pdf_page_poppler(pdf_path, page_num, dpi)


def crop_image(img: Image.Image, bbox: tuple[float, float, float, float]) -> Image.Image:
    """
    Crop PIL Image with either:
    - Normalized fractions (0.0 - 1.0)
    - Absolute pixel coordinates
    """
    w, h = img.size
    x0, y0, x1, y1 = bbox

    # If values are normalized (all <= 1.0), convert to pixels
    if max(x0, y0, x1, y1) <= 1.0:
        px0 = int(round(x0 * w))
        py0 = int(round(y0 * h))
        px1 = int(round(x1 * w))
        py1 = int(round(y1 * h))
    else:
        px0 = int(round(x0))
        py0 = int(round(y0))
        px1 = int(round(x1))
        py1 = int(round(y1))

    # Clamp bounds
    px0 = max(0, min(px0, w))
    py0 = max(0, min(py0, h))
    px1 = max(px0 + 1, min(px1, w))
    py1 = max(py0 + 1, min(py1, h))

    return img.crop((px0, py0, px1, py1))


def main():
    parser = argparse.ArgumentParser(
        description="Crop figures, diagrams, and equations from lecture PDFs or images."
    )
    parser.add_argument("input", help="Path to input PDF or image file")
    parser.add_argument("-p", "--page", type=int, default=1, help="Page number (1-indexed, PDF only; default: 1)")
    parser.add_argument("-o", "--output", help="Output image file (default: assets/<stem>_p<page>_crop.png)")
    parser.add_argument("--dpi", type=int, default=200, help="Rendering DPI for PDF (default: 200, recommend 300 for equations/plots)")
    parser.add_argument("--bbox", help="Bounding box 'x0,y0,x1,y1' (fraction 0.0-1.0 or pixel values)")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help=f"Preset crop region: {', '.join(PRESETS.keys())}")
    parser.add_argument("--full-page", action="store_true", help="Render full page without cropping")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    is_pdf = input_path.suffix.lower() == ".pdf"

    # Load / render image
    if is_pdf:
        try:
            img = render_pdf_page(input_path, args.page, args.dpi)
        except Exception as e:
            print(f"Error rendering PDF page: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            img = Image.open(input_path)
        except Exception as e:
            print(f"Error opening image: {e}", file=sys.stderr)
            sys.exit(1)

    # Determine cropping box
    if args.full_page:
        cropped = img
        tag_desc = "full_page"
    elif args.preset:
        bbox = PRESETS[args.preset]
        cropped = crop_image(img, bbox)
        tag_desc = args.preset
    elif args.bbox:
        bbox = parse_bbox_string(args.bbox)
        cropped = crop_image(img, bbox)
        tag_desc = "crop"
    else:
        # Default: default to full page if nothing specified, with friendly note
        cropped = img
        tag_desc = "full"
        print("Note: No --bbox or --preset specified; rendering full page. Use --preset or --bbox to crop.")

    # Determine output path
    if args.output:
        out_path = Path(args.output)
    else:
        assets_dir = input_path.parent / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        page_suffix = f"_p{args.page}" if is_pdf else ""
        out_path = assets_dir / f"{input_path.stem}{page_suffix}_{tag_desc}.png"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(str(out_path), "PNG")

    print(f"Cropped image saved → {out_path} ({cropped.width}x{cropped.height} px)")
    print(f"\nMarkdown embed snippet:")
    print(f"  ![{out_path.stem}]({out_path.name})")


if __name__ == "__main__":
    main()

