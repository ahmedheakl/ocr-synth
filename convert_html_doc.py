# from docling.document_converter import DocumentConverter
# from docling.datamodel.base_models import InputFormat
# from pathlib import Path

# # Initialize converter with HTML support
# doc_converter = DocumentConverter(
#     allowed_formats=[InputFormat.HTML]
# )

# # Convert HTML file
# html_file = "D:\youssef\synthdocgen\synthdocgen\epub_html_pages\section_029.html"  # or URL
# result = doc_converter.convert(html_file)

# # Export to DocTags
# doctags_output = result.document.export_to_document_tokens()
# print(doctags_output)

# # Save to file with UTF-8 encoding
# with open("output.doctags.txt", "w", encoding="utf-8") as fp:
#     fp.write(doctags_output)

#===========================

# import json
# import re
# from bs4 import BeautifulSoup
# from pathlib import Path
# import hashlib

# class HTMLToDoclingConverter:
#     """
#     Converts HTML files (from EPUB) into Docling document format
#     that can be processed by the synthetic data generation system.
#     """
    
#     def __init__(self):
#         self.document_counter = 0
        
#     def convert_html_file(self, html_file_path: str, output_dir: str):
#         """
#         Convert a single HTML file to Docling document format.
        
#         Args:
#             html_file_path: Path to the HTML file
#             output_dir: Directory to save the converted JSON file
#         """
#         with open(html_file_path, 'r', encoding='utf-8') as f:
#             html_content = f.read()
            
#         # Parse HTML
#         soup = BeautifulSoup(html_content, 'html.parser')
        
#         # Extract content from body
#         body = soup.find('body')
#         if not body:
#             body = soup
            
#         # Convert to Docling format
#         docling_doc = self._convert_to_docling_format(body, html_file_path)
        
#         # Save to JSON file
#         output_path = Path(output_dir) / f"{Path(html_file_path).stem}.json"
#         output_path.parent.mkdir(parents=True, exist_ok=True)
        
#         with open(output_path, 'w', encoding='utf-8') as f:
#             json.dump(docling_doc, f, ensure_ascii=False, indent=2)
            
#         print(f"Converted {html_file_path} -> {output_path}")
#         return str(output_path)
    
#     def _convert_to_docling_format(self, body_element, file_path: str):
#         """Convert HTML body to Docling document format."""
        
#         # Generate document metadata
#         file_name = Path(file_path).name
#         doc_hash = hashlib.md5(file_name.encode()).hexdigest()
        
#         # Initialize Docling document structure
#         docling_doc = {
#             "schema_name": "DoclingDocument",
#             "version": "1.2.0",
#             "name": file_name,
#             "origin": {
#                 "mimetype": "text/html",
#                 "binary_hash": doc_hash,
#                 "filename": file_name
#             },
#             "furnitures": {},
#             "body": {
#                 "self_ref": "#/body",
#                 "children": [],
#                 "content_layer": "body",
#                 "name": "_root_",
#                 "label": "unspecified"
#             },
#             "groups": [],
#             "texts": [],
#             "pictures": [],
#             "tables": [],
#             "key_value_items": [],
#             "form_items": [],
#             "pages": {
#                 "1": {
#                     "size": {"width": 819.0, "height": 1060.0},
#                     "image": {
#                         "mimetype": "image/png",
#                         "dpi": 150,
#                         "size": {"width": 819.0, "height": 1060.0},
#                         "uri": ""
#                     },
#                     "page_no": 1
#                 }
#             }
#         }
        
#         # Process HTML elements
#         text_index = 0
#         for element in body_element.descendants:
#             if element.name and element.string and element.string.strip():
#                 text_content = element.string.strip()
#                 if len(text_content) > 0:
#                     text_item = self._create_text_item(
#                         text_content, 
#                         element.name, 
#                         text_index
#                     )
#                     docling_doc["texts"].append(text_item)
#                     docling_doc["body"]["children"].append({"$ref": f"#/texts/{text_index}"})
#                     text_index += 1
        
#         return docling_doc
    
#     def _create_text_item(self, text: str, html_tag: str, index: int):
#         """Create a text item in Docling format."""
        
#         # Map HTML tags to document labels
#         tag_to_label = {
#             "h1": "section_header",
#             "h2": "section_header", 
#             "h3": "section_header",
#             "h4": "section_header",
#             "h5": "section_header",
#             "h6": "section_header",
#             "p": "paragraph",
#             "div": "paragraph",
#             "span": "text",
#             "strong": "text",
#             "em": "text",
#             "b": "text",
#             "i": "text"
#         }
        
#         label = tag_to_label.get(html_tag, "paragraph")
        
#         return {
#             "self_ref": f"#/texts/{index}",
#             "parent": {"$ref": "#/body"},
#             "children": [],
#             "content_layer": "furniture", 
#             "label": label,
#             "prov": [{
#                 "bbox": {"l": 50, "t": 50 + index * 20, "r": 400, "b": 70 + index * 20, "coord_origin": "TOPLEFT"},
#                 "page_no": 1,
#                 "charspan": [0, len(text)]
#             }],
#             "orig": text,
#             "text": text
#         }

# def convert_html_directory(input_dir: str, output_dir: str):
#     """Convert all HTML files in a directory to Docling format."""
#     converter = HTMLToDoclingConverter()
#     input_path = Path(input_dir)
    
#     html_files = list(input_path.glob("*.html")) + list(input_path.glob("*.htm"))
    
#     for html_file in html_files:
#         converter.convert_html_file(str(html_file), output_dir)
    
#     print(f"Converted {len(html_files)} HTML files to Docling format")

# if __name__ == "__main__":
#     import sys
    
#     if len(sys.argv) != 3:
#         print("Usage: python html_to_docling_converter.py <input_dir> <output_dir>")
#         sys.exit(1)
    
#     input_directory = sys.argv[1]
#     output_directory = sys.argv[2]
    
#     convert_html_directory(input_directory, output_directory)


import json
import re
from bs4 import BeautifulSoup
from pathlib import Path
import hashlib
from tqdm import tqdm
import logging

class HTMLToDoclingConverter:
    """
    Converts HTML files (from EPUB) into Docling document format
    that can be processed by the synthetic data generation system.
    """
    
    def __init__(self, log_file="html_conversion.log"):
        self.document_counter = 0
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_file,
            filemode='w'
        )
        self.logger = logging.getLogger()
        
    def convert_html_file(self, html_file_path: str, output_dir: str):
        """
        Convert a single HTML file to Docling document format.
        
        Args:
            html_file_path: Path to the HTML file
            output_dir: Directory to save the converted JSON file
        """
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract content from body
            body = soup.find('body')
            if not body:
                body = soup
                
            # Convert to Docling format
            docling_doc = self._convert_to_docling_format(body, html_file_path)
            
            # Save to JSON file
            output_path = Path(output_dir) / f"{Path(html_file_path).stem}.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(docling_doc, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"Converted {html_file_path} -> {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Failed to convert {html_file_path}: {e}")
            return None
    
    def _convert_to_docling_format(self, body_element, file_path: str):
        """Convert HTML body to Docling document format."""
        
        # Generate document metadata
        file_name = Path(file_path).name
        doc_hash = hashlib.md5(file_name.encode()).hexdigest()
        
        # Initialize Docling document structure
        docling_doc = {
            "schema_name": "DoclingDocument",
            "version": "1.2.0",
            "name": file_name,
            "origin": {
                "mimetype": "text/html",
                "binary_hash": doc_hash,
                "filename": file_name
            },
            "furnitures": {},
            "body": {
                "self_ref": "#/body",
                "children": [],
                "content_layer": "body",
                "name": "_root_",
                "label": "unspecified"
            },
            "groups": [],
            "texts": [],
            "pictures": [],
            "tables": [],
            "key_value_items": [],
            "form_items": [],
            "pages": {
                "1": {
                    "size": {"width": 819.0, "height": 1060.0},
                    "image": {
                        "mimetype": "image/png",
                        "dpi": 150,
                        "size": {"width": 819.0, "height": 1060.0},
                        "uri": ""
                    },
                    "page_no": 1
                }
            }
        }
        
        # Process HTML elements more comprehensively
        text_index = 0
        
        # Get all text-containing elements, preserving structure
        for element in body_element.find_all(True):
            # Skip elements that are purely containers
            if element.name in ['html', 'head', 'body', 'script', 'style']:
                continue
                
            # Get direct text content (not from children)
            direct_text = element.get_text(strip=True) if element.string else None
            if direct_text and len(direct_text.strip()) > 0:
                text_item = self._create_text_item(
                    direct_text.strip(), 
                    element.name, 
                    text_index
                )
                docling_doc["texts"].append(text_item)
                docling_doc["body"]["children"].append({"$ref": f"#/texts/{text_index}"})
                text_index += 1
        
        # If no structured content found, extract all text
        if text_index == 0:
            all_text = body_element.get_text(strip=True)
            if all_text:
                # Split into paragraphs
                paragraphs = [p.strip() for p in all_text.split('\n\n') if p.strip()]
                for i, paragraph in enumerate(paragraphs):
                    text_item = self._create_text_item(paragraph, "p", i)
                    docling_doc["texts"].append(text_item)
                    docling_doc["body"]["children"].append({"$ref": f"#/texts/{i}"})
        
        return docling_doc
    
    def _create_text_item(self, text: str, html_tag: str, index: int):
        """Create a text item in Docling format."""
        
        # Map HTML tags to document labels
        tag_to_label = {
            "h1": "section_header",
            "h2": "section_header", 
            "h3": "section_header",
            "h4": "section_header",
            "h5": "section_header",
            "h6": "section_header",
            "p": "paragraph",
            "div": "paragraph",
            "span": "text",
            "strong": "text",
            "em": "text",
            "b": "text",
            "i": "text",
            "li": "list_item",
            "blockquote": "paragraph",
            "pre": "paragraph",
            "code": "text"
        }
        
        label = tag_to_label.get(html_tag, "paragraph")
        
        return {
            "self_ref": f"#/texts/{index}",
            "parent": {"$ref": "#/body"},
            "children": [],
            "content_layer": "furniture", 
            "label": label,
            "prov": [{
                "bbox": {"l": 50, "t": 50 + index * 20, "r": 400, "b": 70 + index * 20, "coord_origin": "TOPLEFT"},
                "page_no": 1,
                "charspan": [0, len(text)]
            }],
            "orig": text,
            "text": text
        }

def convert_epub_html_output(epub_html_base_dir: str, output_dir: str):
    """
    Convert all HTML files from EPUB conversion output to Docling format.
    Structure: epub_html_pages/ -> book_name/ -> section_*.html
    
    Args:
        epub_html_base_dir: Base directory containing EPUB-converted HTML subdirectories
        output_dir: Directory to save the converted JSON files
    """
    converter = HTMLToDoclingConverter()
    base_path = Path(epub_html_base_dir)
    output_path = Path(output_dir)
    
    if not base_path.exists():
        print(f"Error: Directory {epub_html_base_dir} does not exist!")
        return
    
    # Find all HTML files recursively in all subdirectories
    html_files = []
    epub_subdirs = [d for d in base_path.iterdir() if d.is_dir()]
    
    print(f"Found {len(epub_subdirs)} EPUB directories to process...")
    
    for subdir in epub_subdirs:
        print(f"  Scanning {subdir.name}...")
        subdir_html_files = list(subdir.glob("*.html")) + list(subdir.glob("*.htm"))
        html_files.extend([(f, subdir.name) for f in subdir_html_files])
        print(f"    Found {len(subdir_html_files)} HTML files")
    
    if not html_files:
        print(f"No HTML files found in any subdirectories of {epub_html_base_dir}")
        return
    
    print(f"\nTotal: {len(html_files)} HTML files to convert")
    
    success_count = 0
    for html_file, epub_name in tqdm(html_files, desc="Converting HTML to Docling", unit="file"):
        # Create output subdirectory for each EPUB
        epub_output_dir = output_path / epub_name
        
        result = converter.convert_html_file(str(html_file), str(epub_output_dir))
        if result:
            success_count += 1
    
    print(f"\nSuccessfully converted {success_count}/{len(html_files)} HTML files to Docling format")
    converter.logger.info(f"Conversion complete: {success_count}/{len(html_files)} files successful")

def convert_single_epub_html_dir(html_dir: str, output_dir: str):
    """Convert HTML files from a single EPUB directory to Docling format."""
    converter = HTMLToDoclingConverter()
    input_path = Path(html_dir)
    
    html_files = list(input_path.glob("*.html")) + list(input_path.glob("*.htm"))
    
    if not html_files:
        print(f"No HTML files found in {html_dir}")
        return
    
    success_count = 0
    for html_file in tqdm(html_files, desc="Converting HTML files", unit="file"):
        result = converter.convert_html_file(str(html_file), output_dir)
        if result:
            success_count += 1
    
    print(f"Converted {success_count}/{len(html_files)} HTML files to Docling format")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        # Original functionality - convert single directory
        input_directory = sys.argv[1]
        output_directory = sys.argv[2]
        convert_single_epub_html_dir(input_directory, output_directory)
        
    elif len(sys.argv) == 4 and sys.argv[1] == "--epub-output":
        # New functionality - convert EPUB HTML output structure
        epub_html_base = sys.argv[2]
        output_directory = sys.argv[3]
        convert_epub_html_output(epub_html_base, output_directory)
        
    else:
        print("Usage:")
        print("  python html_to_docling_converter.py <input_dir> <output_dir>")
        print("  python html_to_docling_converter.py --epub-output <epub_html_base_dir> <output_dir>")
        print("\nFor EPUB output structure, use --epub-output flag")
        sys.exit(1)
        
# usage
# python .\convert_html_doc.py --epub-output ".\epub_html_pages" ".\html_doc"

# python convert_html_doc.py --epub-output "/share/users/ahmed_heakl/ymk/OCR/OCR/urdu_epub_html_pages" "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/urdu/html_doc"