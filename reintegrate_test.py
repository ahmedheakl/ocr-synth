import argparse
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image

from docling_core.types.doc.document import DoclingDocument, ImageRef

def visualize_side_by_side(image: Image.Image, viz: Image.Image) -> Image.Image:
    """Combine image and its visualization side-by-side."""
    w, h = image.size
    viz = viz.resize((w, h))
    combined = Image.new("RGB", (2 * w, h))
    combined.paste(image, (0, 0))
    combined.paste(viz, (w, 0))
    return combined

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", type=str, help="Path to the input PDF file.")
    parser.add_argument("json_path", type=str, help="Path to the DoclingDocument JSON file.")
    parser.add_argument("--out_dir", type=str, default="viz_outputs", help="Directory to save visualizations.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    json_path = Path(args.json_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load PDF and convert to PIL images
    images = convert_from_path(str(pdf_path))
    print(f"{len(images)} pages loaded as PIL images.")

    # Load DoclingDocument
    doc = DoclingDocument.load_from_json(str(json_path))

    # Assign images to pages
    for i in range(1, len(doc.pages) + 1):
        doc.pages[i].image = ImageRef.from_pil(images[i - 1], dpi=72)

    # Get visualization pages
    viz_pages = doc.get_visualization()

    # Combine and save side-by-side visualizations
    for page_num, viz_img in viz_pages.items():
        orig_img = images[page_num - 1]  # zero-based index for images list
        combined = visualize_side_by_side(orig_img, viz_img)
        output_path = out_dir / f"page_{page_num:02d}.png"
        combined.save(output_path)
        print(f"Saved: {output_path}")

    print(doc.export_to_doctags())

if __name__ == "__main__":
    main()