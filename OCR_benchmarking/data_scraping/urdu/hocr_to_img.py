
#!/usr/bin/env python3
"""
Simple usage example for converting your hOCR data to images
"""

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup, FeatureNotFound
import re
import os

def _load_hocr_safely(hocr_file_path):
    # Read raw bytes; do NOT decode here
    with open(hocr_file_path, "rb") as f:
        raw = f.read()

    # Try lxml (best), fall back to html.parser
    for parser in ("lxml", "html.parser"):
        try:
            soup = BeautifulSoup(raw, parser)
            print(f"[hOCR] Parser={parser} | detected encoding={getattr(soup, 'original_encoding', None)}")
            return soup
        except FeatureNotFound:
            continue

    # Last resort: force-decode with common encodings, ignoring errors
    for enc in ("utf-8", "utf-16", "utf-16-le", "utf-16-be", "latin-1"):
        try:
            text = raw.decode(enc, errors="ignore")
            soup = BeautifulSoup(text, "html.parser")
            print(f"[hOCR] Fallback decode with {enc} (errors ignored)")
            return soup
        except Exception:
            pass

    raise RuntimeError("Unable to parse hOCR (encoding and parser attempts failed).")

def simple_hocr_to_images(hocr_file_path, output_dir="page_images"):
    soup = _load_hocr_safely(hocr_file_path)
    os.makedirs(output_dir, exist_ok=True)

    pages = soup.find_all('div', class_='ocr_page')
    print(f"Found {len(pages)} pages")
    for page_num, page in enumerate(pages):
        title = page.get('title', '') or ''
        bbox_match = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', title)
        if not bbox_match:
            print(f"Skipping page {page_num} - no bbox found")
            continue

        x0, y0, x1, y1 = (int(x) for x in bbox_match.groups())
        width, height = max(1, x1 - x0), max(1, y1 - y0)
        print(f"Processing page {page_num}: {width}x{height}")

        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)

        # Try a font that supports Arabic scripts; fallback to default
        font_paths = [
            os.path.expanduser("~/fonts/NotoNastaliqUrdu-Regular.ttf"),
            os.path.expanduser("~/fonts/NotoNaskhArabic-Regular.ttf"),
        ]
        def pick_font(size):
            return ImageFont.truetype(os.path.expanduser("~/fonts/NotoNaskhArabic-Regular.ttf"), size)
            for p in font_paths:
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    continue
            return ImageFont.load_default()

        words = page.find_all('span', class_='ocrx_word')
        for word in words:
            text = (word.get_text() or "").strip()
            if not text:
                continue

            wtitle = word.get('title', '') or ''
            wb = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', wtitle)
            if not wb:
                continue
            wx0, wy0, wx1, wy1 = (int(x) for x in wb.groups())

            # Clamp inside image just in case
            x, y = max(0, wx0 - x0), max(0, wy0 - y0)
            if x >= width or y >= height:
                continue

            fsize = 20
            fsize_m = re.search(r'x_fsize (\d+)', wtitle)
            if fsize_m:
                fsize = min(max(int(fsize_m.group(1)), 10), 60)

            font = pick_font(fsize)

            # NOTE: Pillow doesn't shape Arabic/Urdu; for perfect rendering,
            # integrate `arabic_reshaper` + `python-bidi`. This draws raw glyphs.
            import arabic_reshaper
            from bidi.algorithm import get_display

            def shape_rtl(s: str) -> str:
                return get_display(arabic_reshaper.reshape(s))
            try:
                draw.text((x, y), text, fill='black', font=font)
            except Exception:
                draw.text((x, y), text, fill='black')

        out = os.path.join(output_dir, f"page_{page_num:03d}.png")
        img.save(out)
        print(f"Saved: {out}")

    print(f"Conversion complete! Images saved in {output_dir}")

# Usage example:
if __name__ == "__main__":
    path = "downloaded_hocr/urdumutaradifat/urdumutaradifat_hocr.html"
    simple_hocr_to_images(path, "extracted_pages")