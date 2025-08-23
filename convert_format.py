# import os
# import zipfile
# import shutil
# from pathlib import Path
# from ebooklib import epub, ITEM_DOCUMENT
# from bs4 import BeautifulSoup

# def clean_font_references(content):
#     """Remove all references to missing fonts from OPF content"""
#     soup = BeautifulSoup(content, 'xml')
#     for item in soup.find_all('item'):
#         if 'font' in item.get('media-type', '').lower() or 'font' in item.get('href', '').lower():
#             item.decompose()
#     for style in soup.find_all('style'):
#         if '@font-face' in style.text:
#             style.decompose()
#     return str(soup)

# def extract_epub_items(epub_path):
#     try:
#         book = epub.read_epub(epub_path)
#     except (KeyError, zipfile.BadZipFile) as e:
#         print(f"[Warn] EPUB read failed, attempting repair: {e}")
#         temp_dir = Path("temp_epub_extract")
#         if temp_dir.exists():
#             shutil.rmtree(temp_dir)
#         temp_dir.mkdir()
#         with zipfile.ZipFile(epub_path, 'r') as zf:
#             zf.extractall(temp_dir)
#         for opf_path in temp_dir.rglob("*.opf"):
#             with open(opf_path, "r", encoding="utf-8") as f:
#                 content = f.read()
#             cleaned_content = clean_font_references(content)
#             with open(opf_path, "w", encoding="utf-8") as f:
#                 f.write(cleaned_content)
#         new_epub_path = epub_path.with_name(f"temp_fixed_{epub_path.name}")
#         with zipfile.ZipFile(new_epub_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
#             for file_path in temp_dir.rglob('*'):
#                 if file_path.is_file():
#                     arcname = file_path.relative_to(temp_dir)
#                     zipf.write(file_path, arcname)
#         shutil.rmtree(temp_dir)
#         print(f"[Info] Created repaired EPUB: {new_epub_path}")
#         try:
#             book = epub.read_epub(new_epub_path)
#         finally:
#             if new_epub_path.exists():
#                 os.remove(new_epub_path)

#     items = []
#     for idx, item in enumerate(book.get_items()):
#         if item.get_type() == ITEM_DOCUMENT:
#             try:
#                 content = item.get_content()
#                 soup = BeautifulSoup(content, "html.parser")
#                 items.append((idx, soup))
#             except Exception as e:
#                 print(f"[Warn] Skipping item {item.get_name()}: {e}")
#     return items

# def export_epub_as_html(epub_path, output_dir):
#     output_dir = Path(output_dir)
#     output_dir.mkdir(exist_ok=True, parents=True)
#     epub_path = Path(epub_path)
#     html_chunks = extract_epub_items(epub_path)

#     for idx, soup in html_chunks:
#         html = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <title>EPUB Section {idx}</title>
#   <style>
#     body {{
#       font-family: Arial, sans-serif;
#       padding: 20px;
#       line-height: 1.6;
#     }}
#     img {{
#       max-width: 100%;
#       height: auto;
#     }}
#   </style>
# </head>
# <body>
# {soup.prettify()}
# </body>
# </html>
# """
#         html_filename = f"section_{idx:03d}.html"
#         html_path = output_dir / html_filename
#         with open(html_path, "w", encoding="utf-8") as f:
#             f.write(html)
#         print(f"[Saved] {html_filename}")
#     print(f"[Done] Extracted {len(html_chunks)} HTML files to {output_dir}")

# if __name__ == "__main__":
#     source_dir = Path("D:/youssef/synthdocgen/synthdocgen/synthetic_data_generation/datasets/hindawi_books")
#     for epub_file in source_dir.glob("*.epub"):
#         print(f"\n[Processing] {epub_file.name}")
#         output_subdir = Path("epub_html_pages") / epub_file.stem
#         export_epub_as_html(epub_file, output_dir=output_subdir)

import os
import zipfile
import shutil
from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='epub_conversion.log',
    filemode='w'
)
logger = logging.getLogger()

def clean_font_references(content):
    """Remove all references to missing fonts from OPF content"""
    soup = BeautifulSoup(content, 'xml')
    for item in soup.find_all('item'):
        if 'font' in item.get('media-type', '').lower() or 'font' in item.get('href', '').lower():
            item.decompose()
    for style in soup.find_all('style'):
        if '@font-face' in style.text:
            style.decompose()
    return str(soup)

def extract_epub_items(epub_path):
    try:
        book = epub.read_epub(epub_path)
    except (KeyError, zipfile.BadZipFile, epub.EpubException) as e:
        logger.warning(f"EPUB read failed for {epub_path.name}, attempting repair: {e}")
        temp_dir = Path("temp_epub_extract")
        try:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            temp_dir.mkdir()
            
            try:
                with zipfile.ZipFile(epub_path, 'r') as zf:
                    zf.extractall(temp_dir)
            except (zipfile.BadZipFile, EOFError) as e:
                logger.error(f"Failed to extract {epub_path.name}: {e}")
                return []
            
            opf_found = False
            for opf_path in temp_dir.rglob("*.opf"):
                opf_found = True
                try:
                    with open(opf_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    cleaned_content = clean_font_references(content)
                    with open(opf_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_content)
                except Exception as e:
                    logger.warning(f"Failed to clean OPF file {opf_path}: {e}")
                    continue
            
            if not opf_found:
                logger.error(f"No OPF file found in {epub_path.name}")
                return []
            
            new_epub_path = epub_path.with_name(f"temp_fixed_{epub_path.name}")
            try:
                with zipfile.ZipFile(new_epub_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in temp_dir.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(temp_dir)
                            zipf.write(file_path, arcname)
            except Exception as e:
                logger.error(f"Failed to create repaired EPUB for {epub_path.name}: {e}")
                return []
            
            try:
                book = epub.read_epub(new_epub_path)
            except Exception as e:
                logger.error(f"Failed to read repaired EPUB {new_epub_path.name}: {e}")
                return []
            finally:
                if new_epub_path.exists():
                    try:
                        os.remove(new_epub_path)
                    except Exception as e:
                        logger.warning(f"Failed to delete temporary file {new_epub_path}: {e}")
        finally:
            if temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    logger.warning(f"Failed to delete temporary directory {temp_dir}: {e}")

    items = []
    for idx, item in enumerate(book.get_items()):
        if item.get_type() == ITEM_DOCUMENT:
            try:
                content = item.get_content()
                soup = BeautifulSoup(content, "html.parser")
                items.append((idx, soup))
            except Exception as e:
                logger.warning(f"Skipping item {item.get_name()} in {epub_path.name}: {e}")
    return items

def export_epub_as_html(epub_path, output_dir):
    output_dir = Path(output_dir)
    try:
        output_dir.mkdir(exist_ok=True, parents=True)
        epub_path = Path(epub_path)
        html_chunks = extract_epub_items(epub_path)

        for idx, soup in html_chunks:
            try:
                html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>EPUB Section {idx}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      padding: 20px;
      line-height: 1.6;
    }}
    img {{
      max-width: 100%;
      height: auto;
    }}
  </style>
</head>
<body>
{soup.prettify()}
</body>
</html>
"""
                html_filename = f"section_{idx:03d}.html"
                html_path = output_dir / html_filename
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html)
                logger.info(f"Saved {html_filename}")
            except Exception as e:
                logger.error(f"Failed to save HTML section {idx} for {epub_path.name}: {e}")
                continue
        
        logger.info(f"Extracted {len(html_chunks)} HTML files to {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to process {epub_path.name}: {e}")
        return False

if __name__ == "__main__":
    source_dir = Path("/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/urdu/urdu_epubs")
    output_base = Path("urdu_epub_html_pages")
    
    # Get list of EPUB files with progress bar
    epub_files = list(source_dir.glob("*.epub"))
    if not epub_files:
        logger.error("No EPUB files found in the source directory")
        exit()
    
    # Process files with progress bar
    success_count = 0
    for epub_file in tqdm(epub_files, desc="Processing EPUBs", unit="file"):
        logger.info(f"\nProcessing {epub_file.name}")
        output_subdir = output_base / epub_file.stem
        try:
            if export_epub_as_html(epub_file, output_dir=output_subdir):
                success_count += 1
        except Exception as e:
            logger.error(f"Unexpected error processing {epub_file.name}: {e}")
            continue
    
    logger.info(f"\nProcessing complete. Successfully processed {success_count}/{len(epub_files)} files.")
    print(f"\nDone. Processed {success_count}/{len(epub_files)} files. Check 'epub_conversion.log' for details.")