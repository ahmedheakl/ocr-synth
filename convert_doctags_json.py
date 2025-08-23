# # import json
# # import os
# # import hashlib

# # def doctags_to_docling_json(input_txt_path, output_json_path, filename="original.epub"):
# #     with open(input_txt_path, "r", encoding="utf-8") as f:
# #         lines = f.readlines()

# #     elements = []
# #     element_id = 1
# #     y_position = 100

# #     for line in lines:
# #         line = line.strip()
# #         if line.startswith("<title>") and line.endswith("</title>"):
# #             tag_type = "section"  # instead of "title"
# #             value = line.replace("<title>", "").replace("</title>", "").strip()
# #         elif line.startswith("<text>") and line.endswith("</text>"):
# #             tag_type = "paragraph"  # instead of "text"
# #             value = line.replace("<text>", "").replace("</text>", "").strip()

# #         else:
# #             continue  # skip unrecognized lines

# #         elements.append({
# #             "id": f"p1_e{element_id}",
# #             "type": tag_type,
# #             "label": tag_type,  # <- this is the fix
# #             "value": value,
# #             "position": {"x": 100, "y": y_position}
# #         })
# #         element_id += 1
# #         y_position += 20  # basic vertical spacing

# #     # Generate a dummy hash from filename
# #     binary_hash = hashlib.md5(filename.encode()).hexdigest()

# #     docling_json = {
# #         "schema_name": "docling",
# #         "version": "1.0",
# #         "name": os.path.splitext(os.path.basename(filename))[0],
# #         "origin": {
# #             "filename": filename,
# #             "binary_hash": binary_hash
# #         },
# #         "body": {
# #             "pages": [
# #                 {
# #                     "page_number": 1,
# #                     "elements": elements
# #                 }
# #             ]
# #         }
# #     }

# #     with open(output_json_path, "w", encoding="utf-8") as f:
# #         json.dump(docling_json, f, ensure_ascii=False, indent=2)

# #     print(f"[Done] Converted to Docling JSON: {output_json_path}")

# # # Example usage
# # doctags_to_docling_json(
# #     r"D:\youssef\synthdocgen\synthdocgen\output.doctags.txt", 
# #     "output_docling.json"
# # )

# #!/usr/bin/env python3
# import json
# import re
# from typing import Dict, List, Any


# def convert_doctags_to_json(doctags_string: str) -> Dict[str, Any]:
#     result = {
#         "main_text": [],
#         "text": []
#     }
#     text_counter = 0
#     def add_text_reference(text_content: str) -> Dict[str, str]:
#         nonlocal text_counter
#         result["text"].append({"text": text_content.strip()})
#         ref = {"$ref": f"#/text/{text_counter}"}
#         text_counter += 1
#         return ref
    
#     def clean_text(text: str) -> str:
#         text = re.sub(r'<loc_\d+>', '', text)
#         text = re.sub(r'\s+', ' ', text)
#         return text.strip()
    
#     cleaned_doctags = doctags_string.replace("<end_of_utterance>", "").strip()
#     text_pattern = r'<text[^>]*?>(.*?)</text>'
#     picture_pattern = r'<picture[^>]*?>(.*?)</picture>'
#     table_pattern = r'<table[^>]*?>(.*?)</table>'
#     list_pattern = r'<list[^>]*?>(.*?)</list>'
#     caption_pattern = r'<caption[^>]*?>(.*?)</caption>'
#     all_elements = []
    
#     for match in re.finditer(text_pattern, cleaned_doctags, re.DOTALL):
#         start_pos = match.start()
#         text_content = clean_text(match.group(1))
#         if text_content:
#             all_elements.append((start_pos, {
#                 "label": "paragraph",
#                 "text": text_content
#             }))
    
#     for match in re.finditer(picture_pattern, cleaned_doctags, re.DOTALL):
#         start_pos = match.start()
#         picture_content = match.group(1)
        
#         picture_item = {
#             "label": "figure",
#             "image_path": "images/figure.png"  
#         }
#         captions = []
#         for caption_match in re.finditer(caption_pattern, picture_content, re.DOTALL):
#             caption_text = clean_text(caption_match.group(1))
#             if caption_text:
#                 caption_ref = add_text_reference(caption_text)
#                 captions.append(caption_ref)
        
#         if captions:
#             picture_item["captions"] = captions
        
#         all_elements.append((start_pos, picture_item))
#     for match in re.finditer(table_pattern, cleaned_doctags, re.DOTALL):
#         start_pos = match.start()
#         table_content = match.group(1)
        
#         table_item = {
#             "label": "table"
#         }
#         captions = []
#         for caption_match in re.finditer(caption_pattern, table_content, re.DOTALL):
#             caption_text = clean_text(caption_match.group(1))
#             if caption_text:
#                 caption_ref = add_text_reference(caption_text)
#                 captions.append(caption_ref)
        
#         if captions:
#             table_item["captions"] = captions
        
#         # TODO: Add table data parsing if needed
#         # table_item["data"] = parse_table_data(table_content)
#         all_elements.append((start_pos, table_item))
    
#     for match in re.finditer(list_pattern, cleaned_doctags, re.DOTALL):
#         start_pos = match.start()
#         list_content = match.group(1)
        
#         list_item = {
#             "label": "list",
#             "children": []
#         }
        
#         item_pattern = r'<item[^>]*?>(.*?)</item>'
#         for item_match in re.finditer(item_pattern, list_content, re.DOTALL):
#             item_text = clean_text(item_match.group(1))
#             if item_text:
#                 item_ref = add_text_reference(item_text)
#                 list_item["children"].append(item_ref)
        
#         all_elements.append((start_pos, list_item))
    
#     all_elements.sort(key=lambda x: x[0])
#     result["main_text"] = [element[1] for element in all_elements]
    
#     return result


# def parse_otsl_table(otsl_content: str) -> List[List[str]]:
#     rows = []
#     row_pattern = r'<row[^>]*?>(.*?)</row>'
#     for row_match in re.finditer(row_pattern, otsl_content, re.DOTALL):
#         row_content = row_match.group(1)
#         cell_pattern = r'<cell[^>]*?>(.*?)</cell>'
#         cells = []
#         for cell_match in re.finditer(cell_pattern, row_content, re.DOTALL):
#             cell_text = re.sub(r'<[^>]+>', '', cell_match.group(1)).strip()
#             cells.append(cell_text)
        
#         if cells:
#             rows.append(cells)
    
#     return rows


# def main():
#     with open("D:\youssef\synthdocgen\synthdocgen\output.doctags.txt", "r", encoding="utf-8") as f:
#         sample_doctags = f.read()
    
#     result = convert_doctags_to_json(sample_doctags)
#     print(json.dumps(result, indent=2))
#     with open("output_docling.json", "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2, ensure_ascii=False)
    
#     print("\nSaved to converted_document.json")


# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
# import json
# import re
# from typing import Dict, List, Any
# from pathlib import Path
# from tqdm import tqdm
# import logging

# class DoctagsToJSONConverter:
#     """
#     Converts doctags files to JSON format for synthetic data generation.
#     Handles batch processing of directory structures.
#     """
    
#     def __init__(self, log_file="doctags_conversion.log"):
#         # Set up logging
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s - %(message)s',
#             filename=log_file,
#             filemode='w'
#         )
#         self.logger = logging.getLogger()
    
#     def convert_doctags_to_json(self, doctags_string: str) -> Dict[str, Any]:
#         """Convert doctags string to JSON format."""
#         result = {
#             "main_text": [],
#             "text": []
#         }
#         text_counter = 0
        
#         def add_text_reference(text_content: str) -> Dict[str, str]:
#             nonlocal text_counter
#             result["text"].append({"text": text_content.strip()})
#             ref = {"$ref": f"#/text/{text_counter}"}
#             text_counter += 1
#             return ref
        
#         def clean_text(text: str) -> str:
#             text = re.sub(r'<loc_\d+>', '', text)
#             text = re.sub(r'\s+', ' ', text)
#             return text.strip()
        
#         cleaned_doctags = doctags_string.replace("<end_of_utterance>", "").strip()
#         text_pattern = r'<text[^>]*?>(.*?)</text>'
#         picture_pattern = r'<picture[^>]*?>(.*?)</picture>'
#         table_pattern = r'<table[^>]*?>(.*?)</table>'
#         list_pattern = r'<list[^>]*?>(.*?)</list>'
#         caption_pattern = r'<caption[^>]*?>(.*?)</caption>'
#         all_elements = []
        
#         # Process text elements
#         for match in re.finditer(text_pattern, cleaned_doctags, re.DOTALL):
#             start_pos = match.start()
#             text_content = clean_text(match.group(1))
#             if text_content:
#                 all_elements.append((start_pos, {
#                     "label": "paragraph",
#                     "text": text_content
#                 }))
        
#         # Process picture elements
#         for match in re.finditer(picture_pattern, cleaned_doctags, re.DOTALL):
#             start_pos = match.start()
#             picture_content = match.group(1)
            
#             picture_item = {
#                 "label": "figure",
#                 "image_path": "images/figure.png"  
#             }
#             captions = []
#             for caption_match in re.finditer(caption_pattern, picture_content, re.DOTALL):
#                 caption_text = clean_text(caption_match.group(1))
#                 if caption_text:
#                     caption_ref = add_text_reference(caption_text)
#                     captions.append(caption_ref)
            
#             if captions:
#                 picture_item["captions"] = captions
            
#             all_elements.append((start_pos, picture_item))
        
#         # Process table elements
#         for match in re.finditer(table_pattern, cleaned_doctags, re.DOTALL):
#             start_pos = match.start()
#             table_content = match.group(1)
            
#             table_item = {
#                 "label": "table"
#             }
#             captions = []
#             for caption_match in re.finditer(caption_pattern, table_content, re.DOTALL):
#                 caption_text = clean_text(caption_match.group(1))
#                 if caption_text:
#                     caption_ref = add_text_reference(caption_text)
#                     captions.append(caption_ref)
            
#             if captions:
#                 table_item["captions"] = captions
            
#             # Parse table data if available
#             table_data = self.parse_otsl_table(table_content)
#             if table_data:
#                 table_item["data"] = table_data
            
#             all_elements.append((start_pos, table_item))
        
#         # Process list elements
#         for match in re.finditer(list_pattern, cleaned_doctags, re.DOTALL):
#             start_pos = match.start()
#             list_content = match.group(1)
            
#             list_item = {
#                 "label": "list",
#                 "children": []
#             }
            
#             item_pattern = r'<item[^>]*?>(.*?)</item>'
#             for item_match in re.finditer(item_pattern, list_content, re.DOTALL):
#                 item_text = clean_text(item_match.group(1))
#                 if item_text:
#                     item_ref = add_text_reference(item_text)
#                     list_item["children"].append(item_ref)
            
#             all_elements.append((start_pos, list_item))
        
#         # Sort by position and extract elements
#         all_elements.sort(key=lambda x: x[0])
#         result["main_text"] = [element[1] for element in all_elements]
        
#         return result
    
#     def parse_otsl_table(self, otsl_content: str) -> List[List[str]]:
#         """Parse OTSL table format to structured data."""
#         rows = []
#         row_pattern = r'<row[^>]*?>(.*?)</row>'
#         for row_match in re.finditer(row_pattern, otsl_content, re.DOTALL):
#             row_content = row_match.group(1)
#             cell_pattern = r'<cell[^>]*?>(.*?)</cell>'
#             cells = []
#             for cell_match in re.finditer(cell_pattern, row_content, re.DOTALL):
#                 cell_text = re.sub(r'<[^>]+>', '', cell_match.group(1)).strip()
#                 cells.append(cell_text)
            
#             if cells:
#                 rows.append(cells)
        
#         return rows
    
#     def convert_single_file(self, doctags_file_path: str, output_dir: str):
#         """Convert a single doctags file to JSON."""
#         try:
#             with open(doctags_file_path, 'r', encoding='utf-8') as f:
#                 doctags_content = f.read()
            
#             # Convert to JSON format
#             json_result = self.convert_doctags_to_json(doctags_content)
            
#             # Save JSON file
#             output_path = Path(output_dir) / f"{Path(doctags_file_path).stem}.json"
#             output_path.parent.mkdir(parents=True, exist_ok=True)
            
#             with open(output_path, 'w', encoding='utf-8') as f:
#                 json.dump(json_result, f, ensure_ascii=False, indent=2)
            
#             self.logger.info(f"Converted {doctags_file_path} -> {output_path}")
#             return str(output_path)
            
#         except Exception as e:
#             self.logger.error(f"Failed to convert {doctags_file_path}: {e}")
#             return None

# def convert_doctags_directories(input_base_dir: str, output_dir: str):
#     """
#     Convert all doctags files from directory structure to JSON format.
#     Structure: input_base_dir/ -> book_name/ -> section_*.txt (or *.doctags)
    
#     Args:
#         input_base_dir: Base directory containing subdirectories with doctags files
#         output_dir: Directory to save the converted JSON files
#     """
#     converter = DoctagsToJSONConverter()
#     base_path = Path(input_base_dir)
#     output_path = Path(output_dir)
    
#     if not base_path.exists():
#         print(f"Error: Directory {input_base_dir} does not exist!")
#         return
    
#     # Find all doctags files in subdirectories
#     doctags_files = []
#     subdirs = [d for d in base_path.iterdir() if d.is_dir()]
    
#     print(f"Found {len(subdirs)} directories to process...")
    
#     for subdir in subdirs:
#         print(f"  Scanning {subdir.name}...")
#         # Look for various doctags file extensions
#         subdir_files = (list(subdir.glob("*.txt")) + 
#                        list(subdir.glob("*.doctags")) + 
#                        list(subdir.glob("*.json")))  # In case you have JSON files from previous step
#         doctags_files.extend([(f, subdir.name) for f in subdir_files])
#         print(f"    Found {len(subdir_files)} files")
    
#     if not doctags_files:
#         print(f"No doctags files found in any subdirectories of {input_base_dir}")
#         return
    
#     print(f"\nTotal: {len(doctags_files)} files to convert")
    
#     success_count = 0
#     for doctags_file, book_name in tqdm(doctags_files, desc="Converting doctags to JSON", unit="file"):
#         # Create output subdirectory for each book
#         book_output_dir = output_path / book_name
        
#         result = converter.convert_single_file(str(doctags_file), str(book_output_dir))
#         if result:
#             success_count += 1
    
#     print(f"\nSuccessfully converted {success_count}/{len(doctags_files)} files to JSON format")
#     converter.logger.info(f"Conversion complete: {success_count}/{len(doctags_files)} files successful")

# def convert_single_directory(input_dir: str, output_dir: str):
#     """Convert doctags files from a single directory."""
#     converter = DoctagsToJSONConverter()
#     input_path = Path(input_dir)
    
#     # Look for various file extensions
#     doctags_files = (list(input_path.glob("*.txt")) + 
#                     list(input_path.glob("*.doctags")) + 
#                     list(input_path.glob("*.json")))
    
#     if not doctags_files:
#         print(f"No doctags files found in {input_dir}")
#         return
    
#     success_count = 0
#     for doctags_file in tqdm(doctags_files, desc="Converting files", unit="file"):
#         result = converter.convert_single_file(str(doctags_file), output_dir)
#         if result:
#             success_count += 1
    
#     print(f"Converted {success_count}/{len(doctags_files)} files to JSON format")

# if __name__ == "__main__":
#     import sys
    
#     if len(sys.argv) == 3:
#         # Single directory mode
#         input_directory = sys.argv[1]
#         output_directory = sys.argv[2]
#         convert_single_directory(input_directory, output_directory)
        
#     elif len(sys.argv) == 4 and sys.argv[1] == "--batch":
#         # Batch mode for directory structure
#         input_base = sys.argv[2]
#         output_directory = sys.argv[3]
#         convert_doctags_directories(input_base, output_directory)
        
#     else:
#         print("Usage:")
#         print("  python doctags_converter.py <input_dir> <output_dir>")
#         print("  python doctags_converter.py --batch <input_base_dir> <output_dir>")
#         print("\nFor processing subdirectories with doctags files, use --batch flag")
#         sys.exit(1)


#!/usr/bin/env python3
import json
from typing import Dict, List, Any
from pathlib import Path
from tqdm import tqdm
import logging

class DoclingJSONConverter:
    """
    Converts Docling JSON format to simple JSON format for synthetic data generation.
    Handles batch processing of directory structures.
    """
    
    def __init__(self, log_file="docling_conversion.log"):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_file,
            filemode='w'
        )
        self.logger = logging.getLogger()
    
    def convert_docling_to_simple_json(self, docling_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Docling JSON format to simple JSON format."""
        result = {
            "main_text": [],
            "text": []
        }
        
        # Extract text elements from Docling format
        texts = docling_data.get("texts", [])
        
        for text_item in texts:
            # Extract text content and label
            text_content = text_item.get("text", "") or text_item.get("orig", "")
            label = text_item.get("label", "paragraph")
            
            if text_content.strip():
                # Add to main_text with label
                main_text_item = {
                    "label": label,
                    "text": text_content.strip()
                }
                result["main_text"].append(main_text_item)
                
                # Also add to text array for references
                result["text"].append({"text": text_content.strip()})
        
        # Handle other elements if they exist (tables, pictures, etc.)
        # Add tables
        tables = docling_data.get("tables", [])
        for table in tables:
            table_item = {
                "label": "table"
            }
            # Add table data if available
            if "data" in table:
                table_item["data"] = table["data"]
            
            result["main_text"].append(table_item)
        
        # Add pictures/figures
        pictures = docling_data.get("pictures", [])
        for picture in pictures:
            picture_item = {
                "label": "figure",
                "image_path": picture.get("image_path", "images/figure.png")
            }
            
            # Add captions if available
            if "captions" in picture:
                picture_item["captions"] = picture["captions"]
            
            result["main_text"].append(picture_item)
        
        return result
    
    def convert_single_file(self, docling_file_path: str, output_dir: str):
        """Convert a single Docling JSON file to simple JSON."""
        try:
            with open(docling_file_path, 'r', encoding='utf-8') as f:
                docling_data = json.load(f)
            
            # Convert to simple JSON format
            simple_json = self.convert_docling_to_simple_json(docling_data)
            
            # Save JSON file
            output_path = Path(output_dir) / f"{Path(docling_file_path).stem}.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(simple_json, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Converted {docling_file_path} -> {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Failed to convert {docling_file_path}: {e}")
            return None

def convert_docling_directories(input_base_dir: str, output_dir: str):
    """
    Convert all Docling JSON files from directory structure to simple JSON format.
    Structure: input_base_dir/ -> book_name/ -> section_*.json
    
    Args:
        input_base_dir: Base directory containing subdirectories with Docling JSON files
        output_dir: Directory to save the converted JSON files
    """
    converter = DoclingJSONConverter()
    base_path = Path(input_base_dir)
    output_path = Path(output_dir)
    
    if not base_path.exists():
        print(f"Error: Directory {input_base_dir} does not exist!")
        return
    
    # Find all JSON files in subdirectories
    json_files = []
    subdirs = [d for d in base_path.iterdir() if d.is_dir()]
    
    print(f"Found {len(subdirs)} directories to process...")
    
    for subdir in subdirs:
        print(f"  Scanning {subdir.name}...")
        subdir_files = list(subdir.glob("*.json"))
        json_files.extend([(f, subdir.name) for f in subdir_files])
        print(f"    Found {len(subdir_files)} JSON files")
    
    if not json_files:
        print(f"No JSON files found in any subdirectories of {input_base_dir}")
        return
    
    print(f"\nTotal: {len(json_files)} files to convert")
    
    success_count = 0
    for json_file, book_name in tqdm(json_files, desc="Converting Docling JSON to simple JSON", unit="file"):
        # Create output subdirectory for each book
        book_output_dir = output_path / book_name
        
        result = converter.convert_single_file(str(json_file), str(book_output_dir))
        if result:
            success_count += 1
    
    print(f"\nSuccessfully converted {success_count}/{len(json_files)} files to simple JSON format")
    converter.logger.info(f"Conversion complete: {success_count}/{len(json_files)} files successful")

def convert_single_directory(input_dir: str, output_dir: str):
    """Convert Docling JSON files from a single directory."""
    converter = DoclingJSONConverter()
    input_path = Path(input_dir)
    
    json_files = list(input_path.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return
    
    success_count = 0
    for json_file in tqdm(json_files, desc="Converting files", unit="file"):
        result = converter.convert_single_file(str(json_file), output_dir)
        if result:
            success_count += 1
    
    print(f"Converted {success_count}/{len(json_files)} files to simple JSON format")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        # Single directory mode
        input_directory = sys.argv[1]
        output_directory = sys.argv[2]
        convert_single_directory(input_directory, output_directory)
        
    elif len(sys.argv) == 4 and sys.argv[1] == "--batch":
        # Batch mode for directory structure
        input_base = sys.argv[2]
        output_directory = sys.argv[3]
        convert_docling_directories(input_base, output_directory)
        
    else:
        print("Usage:")
        print("  python docling_json_converter.py <input_dir> <output_dir>")
        print("  python docling_json_converter.py --batch <input_base_dir> <output_dir>")
        print("\nFor processing subdirectories with Docling JSON files, use --batch flag")
        sys.exit(1)

# python convert_doctags_json "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/hebrew/html_doc_mixed" "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/hebrew/hebrew_json"