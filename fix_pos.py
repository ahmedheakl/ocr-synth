# #!/usr/bin/env python3
# """
# Immediate fix script for missing bbox data in DoclingDocument JSON files.
# Run this script to fix your existing generated files.
# """

# import json
# import re
# import os
# import sys
# from typing import Dict, List, Tuple

# def convert_arabic_numerals(arabic_num: str) -> str:
#     """Convert Arabic numerals to Western numerals."""
#     arabic_to_western = {
#         '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
#         '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
#     }
#     western_num = ""
#     for char in arabic_num:
#         western_num += arabic_to_western.get(char, char)
#     return western_num

# def parse_position_file(pos_file_path: str) -> Dict[int, Dict]:
#     """Parse your specific position file format."""
    
#     positions = {}
    
#     if not os.path.exists(pos_file_path):
#         print(f"Position file not found: {pos_file_path}")
#         return positions
    
#     try:
#         with open(pos_file_path, 'r', encoding='utf-8') as f:
#             content = f.read()
        
#         # Parse start and end positions
#         spos_pattern = r'spos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
#         epos_pattern = r'epos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
        
#         spos_matches = re.findall(spos_pattern, content)
#         epos_matches = re.findall(epos_pattern, content)
        
#         print(f"Found {len(spos_matches)} start positions and {len(epos_matches)} end positions")
        
#         # Match start and end positions
#         for spos_match in spos_matches:
#             index, sx, sy, spage = spos_match
#             index = int(index)
            
#             # Find corresponding end position
#             epos_match = next((m for m in epos_matches if m[0] == str(index)), None)
            
#             if epos_match:
#                 _, ex, ey, epage = epos_match
                
#                 # Convert coordinates (scaled points to pixels)
#                 start_x = int(int(sx) / 65536 * 72.27 / 72)  # SP to PT to PX
#                 start_y = int(int(sy) / 65536 * 72.27 / 72)
#                 end_x = int(int(ex) / 65536 * 72.27 / 72)
#                 end_y = int(int(ey) / 65536 * 72.27 / 72)
                
#                 # Convert page number
#                 page_num = int(convert_arabic_numerals(spage))
                
#                 # Calculate bounding box
#                 left = min(start_x, end_x)
#                 right = max(start_x, end_x)
#                 top = min(start_y, end_y)
#                 bottom = max(start_y, end_y)
                
#                 # Ensure minimum dimensions
#                 if right - left < 50:
#                     right = left + 200
#                 if bottom - top < 10:
#                     bottom = top + 25
                
#                 positions[index] = {
#                     'page': page_num,
#                     'bbox': {
#                         'l': left,
#                         't': top,
#                         'r': right,
#                         'b': bottom,
#                         'coord_origin': 'TOPLEFT'
#                     }
#                 }
                
#     except Exception as e:
#         print(f"Error parsing position file: {e}")
    
#     return positions

# def fix_json_file(json_file_path: str, pos_file_path: str) -> str:
#     """Fix missing bbox data in JSON file using position data."""
    
#     # Parse position data
#     positions = parse_position_file(pos_file_path)
    
#     if not positions:
#         print("No position data found - cannot fix JSON file")
#         return None
    
#     # Load JSON file
#     try:
#         with open(json_file_path, 'r', encoding='utf-8') as f:
#             doc_data = json.load(f)
#     except Exception as e:
#         print(f"Error loading JSON file: {e}")
#         return None
    
#     texts = doc_data.get('texts', [])
#     fixed_count = 0
    
#     print(f"Processing {len(texts)} text elements...")
    
#     for i, text_obj in enumerate(texts):
#         # Check if bbox data is missing
#         if not text_obj.get('prov') or len(text_obj['prov']) == 0:
            
#             # Try direct index match first
#             if i in positions:
#                 pos_data = positions[i]
#                 text_obj['prov'] = [{
#                     "bbox": pos_data['bbox'],
#                     "page_no": pos_data['page'],
#                     "charspan": [0, len(text_obj.get('text', ''))]
#                 }]
#                 fixed_count += 1
#                 print(f"✓ Fixed element {i}: '{text_obj.get('text', '')[:30]}...'")
                
#             else:
#                 # Try alternative matching
#                 available_indices = [idx for idx in positions.keys() if idx not in [j for j in range(len(texts)) if texts[j].get('prov')]]
                
#                 if available_indices:
#                     # Use the closest available index
#                     closest_idx = min(available_indices, key=lambda x: abs(x - i))
#                     pos_data = positions[closest_idx]
                    
#                     text_obj['prov'] = [{
#                         "bbox": pos_data['bbox'],
#                         "page_no": pos_data['page'],
#                         "charspan": [0, len(text_obj.get('text', ''))]
#                     }]
#                     fixed_count += 1
#                     print(f"✓ Fixed element {i} (using position {closest_idx}): '{text_obj.get('text', '')[:30]}...'")
#                 else:
#                     print(f"✗ Could not fix element {i}: '{text_obj.get('text', '')[:30]}...'")
    
#     print(f"\nFixed {fixed_count} out of {len([t for t in texts if not t.get('prov')])} missing bbox elements")
    
#     # Save fixed file
#     fixed_file_path = json_file_path.replace('.json', '_fixed.json')
    
#     try:
#         with open(fixed_file_path, 'w', encoding='utf-8') as f:
#             json.dump(doc_data, f, ensure_ascii=False, indent=2)
        
#         print(f"✓ Saved fixed file: {fixed_file_path}")
#         return fixed_file_path
        
#     except Exception as e:
#         print(f"Error saving fixed file: {e}")
#         return None

# def main():
#     """Main function - modify the file paths below to match your files."""
    
#     if len(sys.argv) >= 3:
#         # Command line arguments provided
#         json_file = sys.argv[1]
#         pos_file = sys.argv[2]
#     else:
#         # Default paths - MODIFY THESE TO MATCH YOUR FILES
#         base_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/generated_latex/internal/13052715_section_024_portrait_one_col_arabic_template"
#         instance_num = "0"
        
#         json_file = f"{base_path}_{instance_num}.json"
#         pos_file = f"{base_path}_{instance_num}.pos"
    
#     print("DoclingDocument JSON Bbox Fixer")
#     print("=" * 40)
#     print(f"JSON file: {json_file}")
#     print(f"Position file: {pos_file}")
#     print()
    
#     # Check if files exist
#     if not os.path.exists(json_file):
#         print(f"ERROR: JSON file not found: {json_file}")
#         return
    
#     if not os.path.exists(pos_file):
#         print(f"ERROR: Position file not found: {pos_file}")
#         return
    
#     # Analyze the files first
#     print("Analyzing files...")
    
#     # Check position file
#     with open(pos_file, 'r', encoding='utf-8') as f:
#         pos_content = f.read()
#         pos_lines = len([line for line in pos_content.split('\n') if line.strip()])
    
#     print(f"Position file: {pos_lines} lines")
    
#     # Check JSON file
#     with open(json_file, 'r', encoding='utf-8') as f:
#         json_data = json.load(f)
    
#     texts = json_data.get('texts', [])
#     missing_bbox = len([t for t in texts if not t.get('prov') or len(t['prov']) == 0])
    
#     print(f"JSON file: {len(texts)} text elements, {missing_bbox} missing bbox")
#     print()
    
#     if missing_bbox == 0:
#         print("✓ No missing bbox data found - file is already complete!")
#         return
    
#     # Fix the file
#     print("Fixing missing bbox data...")
#     fixed_file = fix_json_file(json_file, pos_file)
    
#     if fixed_file:
#         print(f"\n✓ SUCCESS: Fixed file saved as {fixed_file}")
        
#         # Verify the fix
#         with open(fixed_file, 'r', encoding='utf-8') as f:
#             fixed_data = json.load(f)
        
#         fixed_texts = fixed_data.get('texts', [])
#         remaining_missing = len([t for t in fixed_texts if not t.get('prov') or len(t['prov']) == 0])
        
#         print(f"Verification: {remaining_missing} elements still missing bbox data")
        
#         if remaining_missing == 0:
#             print("🎉 All bbox data has been successfully restored!")
        
#     else:
#         print("✗ FAILED: Could not fix the file")

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
"""
Improved bbox fixer that works with your visualization workflow.
Includes automatic coordinate system detection and validation.
"""

# import json
# import re
# import os
# import sys
# from typing import Dict, List, Tuple, Optional
# import subprocess

# class SmartCoordinateConverter:
#     """Smart coordinate converter that analyzes existing data to determine the best conversion method."""
    
#     def __init__(self, page_width=819, page_height=1060):
#         self.page_width = page_width
#         self.page_height = page_height
        
#     def analyze_existing_coordinates(self, json_data: dict) -> Dict[str, any]:
#         """Analyze existing bounding boxes to understand the coordinate system."""
        
#         texts = json_data.get('texts', [])
#         existing_bboxes = []
        
#         for text_obj in texts:
#             if text_obj.get('prov') and len(text_obj['prov']) > 0:
#                 bbox = text_obj['prov'][0].get('bbox')
#                 if bbox:
#                     existing_bboxes.append(bbox)
        
#         if not existing_bboxes:
#             return {'error': 'No existing bboxes found for analysis'}
        
#         # Analyze coordinate patterns
#         all_left = [bbox['l'] for bbox in existing_bboxes]
#         all_top = [bbox['t'] for bbox in existing_bboxes]
#         all_right = [bbox['r'] for bbox in existing_bboxes]
#         all_bottom = [bbox['b'] for bbox in existing_bboxes]
        
#         analysis = {
#             'count': len(existing_bboxes),
#             'x_range': (min(all_left), max(all_right)),
#             'y_range': (min(all_top), max(all_bottom)),
#             'avg_width': sum(bbox['r'] - bbox['l'] for bbox in existing_bboxes) / len(existing_bboxes),
#             'avg_height': sum(bbox['b'] - bbox['t'] for bbox in existing_bboxes) / len(existing_bboxes),
#             'coordinate_style': self._detect_coordinate_style(all_left, all_top, all_right, all_bottom)
#         }
        
#         return analysis
    
#     def _detect_coordinate_style(self, left_coords, top_coords, right_coords, bottom_coords):
#         """Detect the coordinate system style based on existing data."""
        
#         max_x = max(max(left_coords), max(right_coords))
#         max_y = max(max(top_coords), max(bottom_coords))
        
#         if max_x <= self.page_width and max_y <= self.page_height:
#             return 'normal_page_coords'
#         elif max_x <= self.page_width * 2 and max_y <= self.page_height * 2:
#             return 'scaled_page_coords'
#         elif max_x > 1000 or max_y > 1000:
#             return 'large_scale_coords'
#         else:
#             return 'unknown'
    
#     def convert_raw_coordinates(self, raw_x: int, raw_y: int, method: str = 'auto') -> Tuple[int, int]:
#         """Convert raw position coordinates to page coordinates."""
        
#         if method == 'auto':
#             method = self._select_best_method(raw_x, raw_y)
        
#         if method == 'sp_to_page_coords':
#             # Convert scaled points to page coordinates
#             # Based on your page dimensions (819 x 1060)
#             pt_x = raw_x / 65536.0  # SP to PT
#             pt_y = raw_y / 65536.0
            
#             # Scale to page coordinates - this needs tuning based on your LaTeX setup
#             # Typical LaTeX page in points is ~612 x 792 (letter size)
#             # Your page is 819 x 1060 pixels
            
#             # Estimate the LaTeX page size in points
#             latex_page_width_pt = 612  # Standard letter width in points
#             latex_page_height_pt = 792  # Standard letter height in points
            
#             # Convert to page coordinates
#             page_x = int((pt_x / latex_page_width_pt) * self.page_width)
#             page_y = int((pt_y / latex_page_height_pt) * self.page_height)
            
#             return page_x, page_y
            
#         elif method == 'proportional_scaling':
#             # Use proportional scaling based on coordinate ranges
#             # This is more reliable when we don't know the exact LaTeX setup
            
#             # These are approximate max values from your data
#             max_raw_x = 35000000  # Observed max X
#             max_raw_y = 46000000  # Observed max Y
            
#             page_x = int((raw_x / max_raw_x) * self.page_width)
#             page_y = int((raw_y / max_raw_y) * self.page_height)
            
#             return page_x, page_y
            
#         elif method == 'inverse_y_proportional':
#             # Same as proportional but flip Y axis (LaTeX origin bottom-left vs top-left)
#             max_raw_x = 35000000
#             max_raw_y = 46000000
            
#             page_x = int((raw_x / max_raw_x) * self.page_width)
#             page_y = self.page_height - int((raw_y / max_raw_y) * self.page_height)
            
#             return page_x, page_y
            
#         else:
#             # Default simple conversion
#             return int(raw_x / 65536), int(raw_y / 65536)
    
#     def _select_best_method(self, raw_x: int, raw_y: int) -> str:
#         """Auto-select the best conversion method based on coordinate magnitude."""
        
#         if raw_x > 10000000 and raw_y > 10000000:
#             return 'proportional_scaling'
#         elif raw_x > 1000000 and raw_y > 1000000:
#             return 'sp_to_page_coords'
#         else:
#             return 'direct_conversion'

# def convert_arabic_numerals(arabic_num: str) -> str:
#     """Convert Arabic numerals to Western numerals."""
#     arabic_to_western = {
#         '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
#         '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
#     }
#     western_num = ""
#     for char in arabic_num:
#         western_num += arabic_to_western.get(char, char)
#     return western_num

# def parse_position_file_smart(pos_file_path: str, converter: SmartCoordinateConverter, 
#                              existing_analysis: dict = None) -> Dict[int, Dict]:
#     """Smart position file parser that adapts to your coordinate system."""
    
#     positions = {}
    
#     if not os.path.exists(pos_file_path):
#         print(f"Position file not found: {pos_file_path}")
#         return positions
    
#     try:
#         with open(pos_file_path, 'r', encoding='utf-8') as f:
#             content = f.read()
        
#         # Parse positions
#         spos_pattern = r'spos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
#         epos_pattern = r'epos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
        
#         spos_matches = re.findall(spos_pattern, content)
#         epos_matches = re.findall(epos_pattern, content)
        
#         print(f"Found {len(spos_matches)} start positions and {len(epos_matches)} end positions")
        
#         # Determine best conversion method based on existing coordinates
#         if existing_analysis and 'coordinate_style' in existing_analysis:
#             style = existing_analysis['coordinate_style']
#             if style == 'normal_page_coords':
#                 conversion_method = 'proportional_scaling'
#             elif style == 'large_scale_coords':
#                 conversion_method = 'sp_to_page_coords'
#             else:
#                 conversion_method = 'proportional_scaling'  # Default
#         else:
#             conversion_method = 'proportional_scaling'
        
#         print(f"Using conversion method: {conversion_method}")
        
#         # Test conversion on first position
#         if spos_matches:
#             test_idx, test_sx, test_sy, test_page = spos_matches[0]
#             test_x, test_y = converter.convert_raw_coordinates(int(test_sx), int(test_sy), conversion_method)
#             print(f"Test conversion - Raw: ({test_sx}, {test_sy}) -> Page: ({test_x}, {test_y})")
            
#             # Check if coordinates seem reasonable
#             if test_x < 0 or test_x > converter.page_width or test_y < 0 or test_y > converter.page_height:
#                 print("WARNING: Test coordinates are outside page bounds, trying alternative method")
#                 conversion_method = 'inverse_y_proportional'
#                 test_x, test_y = converter.convert_raw_coordinates(int(test_sx), int(test_sy), conversion_method)
#                 print(f"Alternative conversion - Raw: ({test_sx}, {test_sy}) -> Page: ({test_x}, {test_y})")
        
#         # Process all positions
#         for spos_match in spos_matches:
#             index, sx, sy, spage = spos_match
#             index = int(index)
            
#             # Find corresponding end position
#             epos_match = next((m for m in epos_matches if m[0] == str(index)), None)
            
#             if epos_match:
#                 _, ex, ey, epage = epos_match
                
#                 # Convert coordinates
#                 start_x, start_y = converter.convert_raw_coordinates(int(sx), int(sy), conversion_method)
#                 end_x, end_y = converter.convert_raw_coordinates(int(ex), int(ey), conversion_method)
                
#                 # Page number
#                 page_num = int(convert_arabic_numerals(spage))
                
#                 # Create bounding box
#                 left = min(start_x, end_x)
#                 right = max(start_x, end_x)
#                 top = min(start_y, end_y)
#                 bottom = max(start_y, end_y)
                
#                 # Ensure minimum dimensions
#                 if right - left < 20:
#                     right = left + 150
#                 if bottom - top < 5:
#                     bottom = top + 20
                
#                 # Clamp to page boundaries
#                 left = max(0, min(left, converter.page_width))
#                 right = min(converter.page_width, max(left + 20, right))
#                 top = max(0, min(top, converter.page_height))
#                 bottom = min(converter.page_height, max(top + 5, bottom))
                
#                 positions[index] = {
#                     'page': page_num,
#                     'bbox': {
#                         'l': left,
#                         't': top,
#                         'r': right,
#                         'b': bottom,
#                         'coord_origin': 'TOPLEFT'
#                     },
#                     'conversion_method': conversion_method
#                 }
                
#     except Exception as e:
#         print(f"Error parsing position file: {e}")
    
#     return positions

# def fix_json_with_validation(json_file_path: str, pos_file_path: str) -> str:
#     """Fix JSON file with built-in validation using your coordinate system."""
    
#     # Load and analyze existing JSON
#     try:
#         with open(json_file_path, 'r', encoding='utf-8') as f:
#             doc_data = json.load(f)
#     except Exception as e:
#         print(f"Error loading JSON file: {e}")
#         return None
    
#     # Get page dimensions from JSON
#     pages = doc_data.get('pages', {})
#     if pages:
#         page1 = pages.get('1', {})
#         page_size = page1.get('size', {})
#         page_width = page_size.get('width', 819)
#         page_height = page_size.get('height', 1060)
#     else:
#         page_width, page_height = 819, 1060
    
#     print(f"Page dimensions: {page_width} x {page_height}")
    
#     # Initialize smart converter
#     converter = SmartCoordinateConverter(page_width, page_height)
    
#     # Analyze existing coordinates
#     existing_analysis = converter.analyze_existing_coordinates(doc_data)
#     if 'error' not in existing_analysis:
#         print("Existing coordinate analysis:")
#         print(f"  Count: {existing_analysis['count']}")
#         print(f"  X range: {existing_analysis['x_range']}")
#         print(f"  Y range: {existing_analysis['y_range']}")
#         print(f"  Style: {existing_analysis['coordinate_style']}")
    
#     # Parse positions with smart conversion
#     positions = parse_position_file_smart(pos_file_path, converter, existing_analysis)
    
#     if not positions:
#         print("No position data found")
#         return None
    
#     # Fix missing bboxes
#     texts = doc_data.get('texts', [])
#     fixed_count = 0
    
#     print(f"\nProcessing {len(texts)} text elements...")
    
#     for i, text_obj in enumerate(texts):
#         if not text_obj.get('prov') or len(text_obj['prov']) == 0:
#             if i in positions:
#                 pos_data = positions[i]
#                 text_obj['prov'] = [{
#                     "bbox": pos_data['bbox'],
#                     "page_no": pos_data['page'],
#                     "charspan": [0, len(text_obj.get('text', ''))]
#                 }]
#                 fixed_count += 1
#                 print(f"✓ Fixed element {i}: {pos_data['bbox']}")
    
#     print(f"\nFixed {fixed_count} elements")
    
#     # Save fixed file
#     fixed_file_path = json_file_path.replace('.json', '_smart_fixed.json')
    
#     try:
#         with open(fixed_file_path, 'w', encoding='utf-8') as f:
#             json.dump(doc_data, f, ensure_ascii=False, indent=2)
        
#         print(f"✓ Saved: {fixed_file_path}")
#         return fixed_file_path
        
#     except Exception as e:
#         print(f"Error saving: {e}")
#         return None

# def auto_visualize_results(json_file_path: str, pdf_path: str = None):
#     """Automatically create visualization using your existing code."""
    
#     base_path = os.path.dirname(json_file_path)
#     json_basename = os.path.splitext(os.path.basename(json_file_path))[0]
    
#     # If PDF path not provided, try to find it
#     if not pdf_path:
#         possible_pdf = json_file_path.replace('.json', '.pdf').replace('_fixed', '').replace('_smart_fixed', '')
#         if os.path.exists(possible_pdf):
#             pdf_path = possible_pdf
    
#     if pdf_path and os.path.exists(pdf_path):
#         print(f"\nConverting PDF to images: {pdf_path}")
        
#         # Create images directory
#         images_dir = os.path.join(base_path, f"{json_basename}_images")
#         os.makedirs(images_dir, exist_ok=True)
        
#         # Convert PDF to images (using your code logic)
#         try:
#             from pdf2image import convert_from_path
#             pages = convert_from_path(pdf_path, 300)
            
#             for i, page in enumerate(pages, start=1):
#                 image_name = f"{json_basename}_{i}.png"
#                 image_path = os.path.join(images_dir, image_name)
#                 page.save(image_path, 'PNG')
#                 print(f"Saved {image_path}")
            
#             # Create bbox visualization
#             output_dir = os.path.join(base_path, f"{json_basename}_bbox_vis")
#             create_bbox_visualization(json_file_path, images_dir, output_dir)
            
#             print(f"\n✓ Visualization complete! Check: {output_dir}")
            
#         except ImportError:
#             print("pdf2image not available, skipping auto-visualization")
#         except Exception as e:
#             print(f"Error in auto-visualization: {e}")

# def create_bbox_visualization(json_file_path: str, images_dir: str, output_dir: str):
#     """Create bbox visualization using simplified version of your code."""
    
#     try:
#         from PIL import Image, ImageDraw, ImageFont
        
#         # Load JSON
#         with open(json_file_path, 'r', encoding='utf-8') as f:
#             data = json.load(f)
        
#         os.makedirs(output_dir, exist_ok=True)
        
#         texts_data = data.get('texts', [])
#         pages_info = data.get('pages', {})
        
#         print(f"Creating visualization for {len(texts_data)} text elements")
        
#         for page_key, page_info in pages_info.items():
#             page_num = int(page_key)
            
#             # Find image file
#             base_name = data.get('name', 'document')
#             image_filename = f"{os.path.basename(json_file_path).replace('.json', '')}_{page_num}.png"
#             image_path = os.path.join(images_dir, image_filename)
            
#             if not os.path.exists(image_path):
#                 print(f"Image not found: {image_path}")
#                 continue
            
#             # Load and process image
#             image = Image.open(image_path)
#             draw = ImageDraw.Draw(image)
#             img_width, img_height = image.size
            
#             # Get scaling factors
#             json_width = page_info.get('size', {}).get('width', 819)
#             json_height = page_info.get('size', {}).get('height', 1060)
#             scale_x = img_width / json_width
#             scale_y = img_height / json_height
            
#             bbox_count = 0
            
#             # Draw bboxes
#             for text_element in texts_data:
#                 if 'prov' in text_element and text_element['prov']:
#                     for prov in text_element['prov']:
#                         if prov.get('page_no') == page_num:
#                             bbox = prov['bbox']
                            
#                             # Scale coordinates
#                             left = bbox['l'] * scale_x
#                             top = bbox['t'] * scale_y
#                             right = bbox['r'] * scale_x
#                             bottom = bbox['b'] * scale_y
                            
#                             # Draw rectangle
#                             draw.rectangle([left, top, right, bottom], 
#                                          outline=(0, 255, 0), width=2)
                            
#                             # Add label
#                             element_id = text_element.get('self_ref', '').split('/')[-1]
#                             label = f"T{element_id}"
                            
#                             try:
#                                 font = ImageFont.load_default()
#                                 draw.text((left, max(0, top - 15)), label, 
#                                         fill=(0, 255, 0), font=font)
#                             except:
#                                 draw.text((left, max(0, top - 15)), label, 
#                                         fill=(0, 255, 0))
                            
#                             bbox_count += 1
            
#             # Save result
#             output_filename = f"page_{page_num}_with_boxes.png"
#             output_path = os.path.join(output_dir, output_filename)
#             image.save(output_path)
            
#             print(f"Page {page_num}: {bbox_count} boxes -> {output_path}")
            
#     except Exception as e:
#         print(f"Error creating visualization: {e}")

# def main():
#     """Main function with automatic workflow."""
    
#     if len(sys.argv) >= 3:
#         json_file = sys.argv[1]
#         pos_file = sys.argv[2]
#         pdf_file = sys.argv[3] if len(sys.argv) > 3 else None
#     else:
#         # Default paths
#         base_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/generated_latex/internal/13052715_section_024_portrait_one_col_arabic_template"
#         instance_num = "0"
        
#         json_file = f"{base_path}_{instance_num}.json"
#         pos_file = f"{base_path}_{instance_num}.pos"
#         pdf_file = f"{base_path}_{instance_num}.pdf"
    
#     print("Smart Bbox Fixer with Visualization")
#     print("=" * 50)
#     print(f"JSON: {json_file}")
#     print(f"POS: {pos_file}")
#     print(f"PDF: {pdf_file}")
#     print()
    
#     # Check files
#     if not os.path.exists(json_file):
#         print(f"ERROR: JSON file not found")
#         return
    
#     if not os.path.exists(pos_file):
#         print(f"ERROR: Position file not found")
#         return
    
#     # Fix the JSON
#     fixed_file = fix_json_with_validation(json_file, pos_file)
    
#     if fixed_file:
#         print(f"\n✓ Fixed file created: {fixed_file}")
        
#         # Auto-create visualization
#         auto_visualize_results(fixed_file, pdf_file)
        
#     else:
#         print("✗ Failed to fix file")

# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3
"""
Corrected coordinate converter that properly interprets your position data.
"""

import json
import re
import os
import sys
from typing import Dict, List, Tuple

def convert_arabic_numerals(arabic_num: str) -> str:
    """Convert Arabic numerals to Western numerals."""
    arabic_to_western = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    western_num = ""
    for char in arabic_num:
        western_num += arabic_to_western.get(char, char)
    return western_num

def analyze_coordinate_system(json_data: dict, pos_data: list) -> dict:
    """Analyze both JSON and position data to determine correct coordinate mapping."""
    
    # Get existing bbox ranges from JSON
    texts = json_data.get('texts', [])
    existing_bboxes = []
    
    for text_obj in texts:
        if text_obj.get('prov') and len(text_obj['prov']) > 0:
            bbox = text_obj['prov'][0].get('bbox')
            if bbox:
                existing_bboxes.append(bbox)
    
    if not existing_bboxes:
        return {'error': 'No existing bboxes for reference'}
    
    # Analyze JSON coordinate system
    json_left = [bbox['l'] for bbox in existing_bboxes]
    json_right = [bbox['r'] for bbox in existing_bboxes]
    json_top = [bbox['t'] for bbox in existing_bboxes]
    json_bottom = [bbox['b'] for bbox in existing_bboxes]
    
    json_analysis = {
        'x_range': (min(json_left), max(json_right)),
        'y_range': (min(json_top), max(json_bottom)),
        'left_margin': min(json_left),
        'typical_width': max(json_right) - min(json_left)
    }
    
    # Analyze position data coordinate system
    if not pos_data:
        return {'error': 'No position data'}
    
    pos_start_x = [item['start_x'] for item in pos_data]
    pos_end_x = [item['end_x'] for item in pos_data]
    pos_start_y = [item['start_y'] for item in pos_data]
    pos_end_y = [item['end_y'] for item in pos_data]
    
    pos_analysis = {
        'start_x_range': (min(pos_start_x), max(pos_start_x)),
        'end_x_range': (min(pos_end_x), max(pos_end_x)),
        'y_range': (min(pos_start_y + pos_end_y), max(pos_start_y + pos_end_y)),
        'consistent_left_margin': len(set(pos_start_x)) == 1,  # All start X same?
        'x_span': max(pos_end_x) - min(pos_start_x)
    }
    
    return {
        'json': json_analysis,
        'pos': pos_analysis,
        'page_width': json_data.get('pages', {}).get('1', {}).get('size', {}).get('width', 819),
        'page_height': json_data.get('pages', {}).get('1', {}).get('size', {}).get('height', 1060)
    }

def calculate_conversion_mapping(analysis: dict) -> dict:
    """Calculate the coordinate conversion mapping."""
    
    json_info = analysis['json']
    pos_info = analysis['pos']
    page_width = analysis['page_width']
    page_height = analysis['page_height']
    
    # X-axis mapping
    # Position data spans from min(start_x, end_x) to max(start_x, end_x)
    pos_x_min = min(pos_info['start_x_range'][0], pos_info['end_x_range'][0])
    pos_x_max = max(pos_info['start_x_range'][1], pos_info['end_x_range'][1])
    pos_x_span = pos_x_max - pos_x_min
    
    # JSON data spans from left margin to right edge
    json_x_min = json_info['left_margin']
    json_x_max = json_info['x_range'][1]
    json_x_span = json_x_max - json_x_min
    
    # Y-axis mapping (might need flipping)
    pos_y_min = pos_info['y_range'][0]
    pos_y_max = pos_info['y_range'][1]
    pos_y_span = pos_y_max - pos_y_min
    
    json_y_min = json_info['y_range'][0]
    json_y_max = json_info['y_range'][1]
    json_y_span = json_y_max - json_y_min
    
    return {
        'x_scale': json_x_span / pos_x_span if pos_x_span > 0 else 1,
        'y_scale': json_y_span / pos_y_span if pos_y_span > 0 else 1,
        'x_offset': json_x_min - (pos_x_min * (json_x_span / pos_x_span)) if pos_x_span > 0 else 0,
        'y_offset': json_y_min,
        'pos_x_range': (pos_x_min, pos_x_max),
        'pos_y_range': (pos_y_min, pos_y_max),
        'json_x_range': json_info['x_range'],
        'json_y_range': json_info['y_range'],
        'flip_y': False  # We'll test both orientations
    }

def convert_coordinates(pos_x: int, pos_y: int, mapping: dict) -> tuple:
    """Convert position coordinates to JSON page coordinates."""
    
    # Convert X
    json_x = int((pos_x - mapping['pos_x_range'][0]) * mapping['x_scale'] + mapping['json_x_range'][0])
    
    # Convert Y (test both orientations)
    if mapping['flip_y']:
        # Flip Y axis (LaTeX bottom-left to JSON top-left)
        pos_y_normalized = (pos_y - mapping['pos_y_range'][0]) / (mapping['pos_y_range'][1] - mapping['pos_y_range'][0])
        json_y = int(mapping['json_y_range'][1] - (pos_y_normalized * (mapping['json_y_range'][1] - mapping['json_y_range'][0])))
    else:
        # Direct Y mapping
        json_y = int((pos_y - mapping['pos_y_range'][0]) * mapping['y_scale'] + mapping['json_y_range'][0])
    
    # Clamp to page bounds
    json_x = max(0, min(json_x, 819))
    json_y = max(0, min(json_y, 1060))
    
    return json_x, json_y

def calculate_conversion_mapping(analysis: dict) -> dict:
    """Calculate the coordinate conversion mapping."""
    
    json_info = analysis['json']
    pos_info = analysis['pos']
    page_height = analysis['page_height']
    
    # X-axis mapping
    pos_x_min = min(pos_info['start_x_range'][0], pos_info['end_x_range'][0])
    pos_x_max = max(pos_info['start_x_range'][1], pos_info['end_x_range'][1])
    pos_x_span = pos_x_max - pos_x_min
    
    json_x_min = json_info['left_margin']
    json_x_max = json_info['x_range'][1]
    json_x_span = json_x_max - json_x_min
    
    # Y-axis mapping - we'll assume position data is bottom-left origin
    pos_y_min = pos_info['y_range'][0]
    pos_y_max = pos_info['y_range'][1]
    pos_y_span = pos_y_max - pos_y_min
    
    json_y_min = json_info['y_range'][0]
    json_y_max = json_info['y_range'][1]
    json_y_span = json_y_max - json_y_min
    
    return {
        'x_scale': json_x_span / pos_x_span if pos_x_span > 0 else 1,
        'y_scale': json_y_span / pos_y_span if pos_y_span > 0 else 1,
        'x_offset': json_x_min - (pos_x_min * (json_x_span / pos_x_span)) if pos_x_span > 0 else 0,
        'y_offset': json_y_min,
        'pos_x_range': (pos_x_min, pos_x_max),
        'pos_y_range': (pos_y_min, pos_y_max),
        'json_x_range': json_info['x_range'],
        'json_y_range': json_info['y_range'],
        'flip_y': True,  # Always flip Y since position data is likely bottom-left origin
        'page_height': page_height
    }

def convert_coordinates(pos_x: int, pos_y: int, mapping: dict) -> tuple:
    """Convert position coordinates to JSON page coordinates."""
    
    # Convert X
    json_x = int((pos_x - mapping['pos_x_range'][0]) * mapping['x_scale'] + mapping['json_x_range'][0])
    
    # Convert Y - always flip since position data is bottom-left origin
    if mapping['flip_y']:
        # Normalize position Y (0-1 range)
        pos_y_normalized = (pos_y - mapping['pos_y_range'][0]) / (mapping['pos_y_range'][1] - mapping['pos_y_range'][0])
        # Flip and scale to JSON coordinates
        json_y = int(mapping['json_y_range'][1] - (pos_y_normalized * (mapping['json_y_range'][1] - mapping['json_y_range'][0])))
    else:
        # Direct mapping (unlikely to be correct)
        json_y = int((pos_y - mapping['pos_y_range'][0]) * mapping['y_scale'] + mapping['json_y_range'][0])
    
    # Clamp to page bounds
    json_x = max(0, min(json_x, mapping.get('page_width', 819)))
    json_y = max(0, min(json_y, mapping.get('page_height', 1060)))
    
    return json_x, json_y

def parse_position_file_corrected(pos_file_path: str) -> List[dict]:
    """Parse position file with correct understanding of the format."""
    
    positions = []
    
    if not os.path.exists(pos_file_path):
        print(f"Position file not found: {pos_file_path}")
        return positions
    
    try:
        with open(pos_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse all positions
        spos_pattern = r'spos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
        epos_pattern = r'epos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
        
        spos_matches = re.findall(spos_pattern, content)
        epos_matches = re.findall(epos_pattern, content)
        
        print(f"Found {len(spos_matches)} start positions and {len(epos_matches)} end positions")
        
        # Match start and end positions
        for spos_match in spos_matches:
            index, sx, sy, spage = spos_match
            index = int(index)
            
            # Find corresponding end position
            epos_match = next((m for m in epos_matches if m[0] == str(index)), None)
            
            if epos_match:
                _, ex, ey, epage = epos_match
                
                page_num = int(convert_arabic_numerals(spage))
                
                positions.append({
                    'index': index,
                    'start_x': int(sx),
                    'start_y': int(sy),
                    'end_x': int(ex),
                    'end_y': int(ey),
                    'page': page_num
                })
        
        # Sort by index to maintain order
        positions.sort(key=lambda x: x['index'])
        
    except Exception as e:
        print(f"Error parsing position file: {e}")
    
    return positions

def fix_json_with_corrected_conversion(json_file_path: str, pos_file_path: str) -> str:
    """Fix JSON using corrected coordinate conversion."""
    
    print("Corrected Coordinate Converter")
    print("=" * 40)
    
    # Load JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            doc_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    
    # Parse position data
    pos_data = parse_position_file_corrected(pos_file_path)
    
    if not pos_data:
        print("No position data found")
        return None
    
    print(f"Parsed {len(pos_data)} position entries")
    
    # Analyze coordinate systems
    analysis = analyze_coordinate_system(doc_data, pos_data)
    
    if 'error' in analysis:
        print(f"Analysis error: {analysis['error']}")
        return None
    
    print("\nCoordinate System Analysis:")
    print(f"JSON X range: {analysis['json']['x_range']}")
    print(f"JSON Y range: {analysis['json']['y_range']}")
    print(f"Position X range: {analysis['pos']['start_x_range']} to {analysis['pos']['end_x_range']}")
    print(f"Position Y range: {analysis['pos']['y_range']}")
    print(f"Consistent left margin: {analysis['pos']['consistent_left_margin']}")
    
    # Calculate conversion mapping
    mapping = calculate_conversion_mapping(analysis)
    
    print(f"\nConversion Mapping:")
    print(f"X scale: {mapping['x_scale']:.6f}")
    print(f"Y scale: {mapping['y_scale']:.6f}")
    
    # Test conversion on first few positions
    print(f"\nTesting coordinate conversion:")
    for i, pos_item in enumerate(pos_data[:3]):
        start_json_x, start_json_y = convert_coordinates(pos_item['start_x'], pos_item['start_y'], mapping)
        end_json_x, end_json_y = convert_coordinates(pos_item['end_x'], pos_item['end_y'], mapping)
        
        print(f"Position {pos_item['index']}:")
        print(f"  Raw: start({pos_item['start_x']}, {pos_item['start_y']}) end({pos_item['end_x']}, {pos_item['end_y']})")
        print(f"  JSON: start({start_json_x}, {start_json_y}) end({end_json_x}, {end_json_y})")
        
        # Check if this looks reasonable
        reasonable = (0 <= start_json_x <= 819 and 0 <= start_json_y <= 1060 and
                     0 <= end_json_x <= 819 and 0 <= end_json_y <= 1060)
        print(f"  Reasonable: {'✓' if reasonable else '✗'}")
    
    # If initial conversion doesn't look good, try Y-flip
    first_pos = pos_data[0]
    test_x, test_y = convert_coordinates(first_pos['start_x'], first_pos['start_y'], mapping)
    
    if test_y > 800:  # Seems too low, try Y-flip
        print("\nTrying Y-flip conversion...")
        mapping['flip_y'] = True
        
        test_x, test_y = convert_coordinates(first_pos['start_x'], first_pos['start_y'], mapping)
        print(f"Y-flipped result: ({test_x}, {test_y})")
    
    # Apply conversion to missing texts
    texts = doc_data.get('texts', [])
    fixed_count = 0
    
    print(f"\nFixing missing bboxes...")
    
    for i, text_obj in enumerate(texts):
        if not text_obj.get('prov') or len(text_obj['prov']) == 0:
            # Find corresponding position data
            if i < len(pos_data):
                pos_item = pos_data[i]
                
                # Convert coordinates
                start_x, start_y = convert_coordinates(pos_item['start_x'], pos_item['start_y'], mapping)
                end_x, end_y = convert_coordinates(pos_item['end_x'], pos_item['end_y'], mapping)
                
                # Create bbox
                left = min(start_x, end_x)
                right = max(start_x, end_x)
                top = min(start_y, end_y)
                bottom = max(start_y, end_y)
                
                # Ensure minimum dimensions
                if right - left < 20:
                    right = left + 150
                if bottom - top < 5:
                    bottom = top + 20
                
                bbox = {
                    'l': left,
                    't': top,
                    'r': right,
                    'b': bottom,
                    'coord_origin': 'TOPLEFT'
                }
                
                text_obj['prov'] = [{
                    "bbox": bbox,
                    "page_no": pos_item['page'],
                    "charspan": [0, len(text_obj.get('text', ''))]
                }]
                
                fixed_count += 1
                
                text_preview = text_obj.get('text', '')[:40] + "..."
                print(f"✓ Fixed element {i}: {bbox} - '{text_preview}'")
    
    print(f"\nFixed {fixed_count} text elements")
    
    # Save fixed file
    fixed_file_path = json_file_path.replace('.json', '_coordinate_fixed.json')
    
    try:
        with open(fixed_file_path, 'w', encoding='utf-8') as f:
            json.dump(doc_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved: {fixed_file_path}")
        return fixed_file_path
        
    except Exception as e:
        print(f"Error saving: {e}")
        return None

def main():
    """Main function."""
    
    if len(sys.argv) >= 3:
        json_file = sys.argv[1]
        pos_file = sys.argv[2]
    else:
        # Default paths
        base_path = "synthetic_data_generation/generated_latex/internal/13052715_section_024_portrait_one_col_arabic_template"
        json_file = f"{base_path}_0.json"
        pos_file = f"{base_path}_0.pos"
    
    print(f"JSON file: {json_file}")
    print(f"Position file: {pos_file}")
    
    if not os.path.exists(json_file):
        print(f"ERROR: JSON file not found")
        return
    
    if not os.path.exists(pos_file):
        print(f"ERROR: Position file not found")
        return
    
    fixed_file = fix_json_with_corrected_conversion(json_file, pos_file)
    
    if fixed_file:
        print(f"\n✅ SUCCESS!")
        print(f"Fixed file: {fixed_file}")
        print(f"\nNow test with your visualization script!")
    else:
        print("❌ FAILED")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# """
# Fine-tuner for bbox coordinates - allows quick Y-axis adjustments.
# Since the boxes are "slightly down from the right place", this will help you dial in the exact position.
# """

# import json
# import os
# import sys
# from typing import List, Dict

# def load_json_file(file_path: str) -> dict:
#     """Load JSON file safely."""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     except Exception as e:
#         print(f"Error loading {file_path}: {e}")
#         return None

# def identify_fixed_elements(json_data: dict) -> List[dict]:
#     """Identify which elements were recently fixed (likely the problematic ones)."""
    
#     texts = json_data.get('texts', [])
    
#     # Look for elements that might be the newly fixed ones
#     # Strategy: find elements with bboxes that don't follow the typical pattern
    
#     all_elements_with_bbox = []
#     for i, text_obj in enumerate(texts):
#         if text_obj.get('prov') and len(text_obj['prov']) > 0:
#             bbox = text_obj['prov'][0]['bbox']
#             all_elements_with_bbox.append({
#                 'index': i,
#                 'text_obj': text_obj,
#                 'bbox': bbox,
#                 'y_position': bbox['t'],
#                 'text_preview': text_obj.get('text', '')[:50] + "..."
#             })
    
#     # Sort by Y position to see the order
#     all_elements_with_bbox.sort(key=lambda x: x['y_position'])
    
#     # Try to identify the newly added ones
#     # They might be at unusual Y positions or have different patterns
    
#     print("All elements with bboxes (sorted by Y position):")
#     for i, elem in enumerate(all_elements_with_bbox):
#         print(f"  {i}: Y={elem['y_position']} - '{elem['text_preview']}'")
    
#     # Look for gaps or unusual positions
#     y_positions = [elem['y_position'] for elem in all_elements_with_bbox]
    
#     if len(y_positions) > 1:
#         y_gaps = [y_positions[i+1] - y_positions[i] for i in range(len(y_positions)-1)]
#         avg_gap = sum(y_gaps) / len(y_gaps) if y_gaps else 0
        
#         print(f"\nAverage Y gap between elements: {avg_gap:.1f}")
        
#         # Elements with unusual gaps might be the fixed ones
#         unusual_elements = []
#         for i, gap in enumerate(y_gaps):
#             if gap > avg_gap * 1.5:  # Much larger gap
#                 unusual_elements.append(all_elements_with_bbox[i+1])
        
#         if unusual_elements:
#             print(f"\nElements with unusual positioning (likely the fixed ones):")
#             return unusual_elements
    
#     # Fallback: return last few elements (likely the newly added ones)
#     return all_elements_with_bbox[-2:] if len(all_elements_with_bbox) >= 2 else all_elements_with_bbox

# def adjust_y_coordinates(json_data: dict, y_offset: int, elements_to_adjust: List[dict] = None) -> dict:
#     """Adjust Y coordinates of specified elements or all elements."""
    
#     texts = json_data.get('texts', [])
#     adjusted_count = 0
    
#     if elements_to_adjust:
#         # Adjust only specific elements
#         indices_to_adjust = [elem['index'] for elem in elements_to_adjust]
        
#         for i, text_obj in enumerate(texts):
#             if i in indices_to_adjust and text_obj.get('prov') and len(text_obj['prov']) > 0:
#                 for prov in text_obj['prov']:
#                     if 'bbox' in prov:
#                         bbox = prov['bbox']
#                         old_top = bbox['t']
#                         old_bottom = bbox['b']
                        
#                         # Adjust Y coordinates
#                         bbox['t'] = max(0, old_top + y_offset)
#                         bbox['b'] = max(bbox['t'] + 5, old_bottom + y_offset)
                        
#                         # Clamp to page bounds
#                         bbox['t'] = min(1060, bbox['t'])
#                         bbox['b'] = min(1060, bbox['b'])
                        
#                         adjusted_count += 1
                        
#                         text_preview = text_obj.get('text', '')[:30] + "..."
#                         print(f"  Adjusted element {i}: {old_top} → {bbox['t']} - '{text_preview}'")
#     else:
#         # Adjust all elements (global adjustment)
#         for text_obj in texts:
#             if text_obj.get('prov') and len(text_obj['prov']) > 0:
#                 for prov in text_obj['prov']:
#                     if 'bbox' in prov:
#                         bbox = prov['bbox']
#                         bbox['t'] = max(0, bbox['t'] + y_offset)
#                         bbox['b'] = max(bbox['t'] + 5, bbox['b'] + y_offset)
                        
#                         # Clamp to page bounds
#                         bbox['t'] = min(1060, bbox['t'])
#                         bbox['b'] = min(1060, bbox['b'])
                        
#                         adjusted_count += 1
    
#     print(f"Adjusted {adjusted_count} bbox elements")
#     return json_data

# def create_multiple_test_versions(json_file_path: str, test_offsets: List[int]) -> List[str]:
#     """Create multiple test versions with different Y offsets."""
    
#     original_data = load_json_file(json_file_path)
#     if not original_data:
#         return []
    
#     created_files = []
#     base_name = json_file_path.replace('.json', '')
    
#     for offset in test_offsets:
#         # Create a copy of the data
#         test_data = json.loads(json.dumps(original_data))
        
#         # Identify elements to adjust
#         elements_to_adjust = identify_fixed_elements(test_data)
        
#         print(f"\nCreating test version with Y offset: {offset:+d}")
        
#         # Apply adjustment
#         adjusted_data = adjust_y_coordinates(test_data, offset, elements_to_adjust)
        
#         # Save test version
#         test_file_path = f"{base_name}_y_offset_{offset:+d}.json"
        
#         try:
#             with open(test_file_path, 'w', encoding='utf-8') as f:
#                 json.dump(adjusted_data, f, ensure_ascii=False, indent=2)
            
#             created_files.append(test_file_path)
#             print(f"✓ Created: {test_file_path}")
            
#         except Exception as e:
#             print(f"✗ Error creating {test_file_path}: {e}")
    
#     return created_files

# def interactive_fine_tuning(json_file_path: str):
#     """Interactive fine-tuning of bbox positions."""
    
#     print("INTERACTIVE BBOX FINE-TUNING")
#     print("=" * 40)
#     print(f"Working with: {json_file_path}")
    
#     original_data = load_json_file(json_file_path)
#     if not original_data:
#         return
    
#     # Identify elements that need adjustment
#     print("\nIdentifying elements to adjust...")
#     elements_to_adjust = identify_fixed_elements(original_data)
    
#     if not elements_to_adjust:
#         print("No elements found to adjust")
#         return
    
#     print(f"\nFound {len(elements_to_adjust)} elements that may need adjustment:")
#     for elem in elements_to_adjust:
#         print(f"  - Y={elem['y_position']}: '{elem['text_preview']}'")
    
#     print(f"\nOptions:")
#     print("1. Create multiple test versions with different offsets")
#     print("2. Apply a specific Y offset")
#     print("3. Adjust all elements globally")
    
#     try:
#         choice = input("\nEnter choice (1-3): ").strip()
        
#         if choice == "1":
#             # Create multiple test versions
#             test_offsets = [-30, -20, -15, -10, -5, +5, +10, +15, +20, +30]
#             print(f"\nCreating test versions with offsets: {test_offsets}")
            
#             created_files = create_multiple_test_versions(json_file_path, test_offsets)
            
#             print(f"\n✅ Created {len(created_files)} test versions!")
#             print("Now run your visualization script on each to see which looks best:")
#             for file_path in created_files:
#                 print(f"  {file_path}")
            
#         elif choice == "2":
#             # Apply specific offset
#             offset_str = input("Enter Y offset (negative = move up, positive = move down): ").strip()
#             try:
#                 y_offset = int(offset_str)
                
#                 print(f"\nApplying Y offset: {y_offset:+d}")
                
#                 # Create adjusted version
#                 adjusted_data = json.loads(json.dumps(original_data))
#                 adjusted_data = adjust_y_coordinates(adjusted_data, y_offset, elements_to_adjust)
                
#                 # Save adjusted version
#                 output_file = json_file_path.replace('.json', f'_adjusted_{y_offset:+d}.json')
                
#                 with open(output_file, 'w', encoding='utf-8') as f:
#                     json.dump(adjusted_data, f, ensure_ascii=False, indent=2)
                
#                 print(f"✓ Created: {output_file}")
                
#             except ValueError:
#                 print("Invalid offset value")
                
#         elif choice == "3":
#             # Global adjustment
#             offset_str = input("Enter Y offset for ALL elements: ").strip()
#             try:
#                 y_offset = int(offset_str)
                
#                 print(f"\nApplying global Y offset: {y_offset:+d}")
                
#                 adjusted_data = json.loads(json.dumps(original_data))
#                 adjusted_data = adjust_y_coordinates(adjusted_data, y_offset, None)  # None = all elements
                
#                 output_file = json_file_path.replace('.json', f'_global_adjusted_{y_offset:+d}.json')
                
#                 with open(output_file, 'w', encoding='utf-8') as f:
#                     json.dump(adjusted_data, f, ensure_ascii=False, indent=2)
                
#                 print(f"✓ Created: {output_file}")
                
#             except ValueError:
#                 print("Invalid offset value")
        
#         else:
#             print("Invalid choice")
            
#     except KeyboardInterrupt:
#         print("\nCancelled by user")

# def quick_fix_suggestions():
#     """Provide quick fix suggestions based on common issues."""
    
#     print(f"\nQUICK FIX SUGGESTIONS:")
#     print("=" * 30)
#     print("If boxes are 'slightly down from right place':")
#     print("  • Try Y offset: -10 to -20 (move up)")
#     print("  • This is often due to baseline/line-height differences")
#     print()
#     print("If boxes are too far down:")
#     print("  • Try Y offset: -30 to -50")
#     print()
#     print("If boxes are too far up:")
#     print("  • Try Y offset: +10 to +30")
#     print()
#     print("Test multiple offsets and use your visualization script to check results!")

# def main():
#     """Main function."""
    
#     if len(sys.argv) >= 2:
#         json_file = sys.argv[1]
#     else:
#         # Default to the coordinate-fixed file
#         base_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/generated_latex/internal/13052715_section_024_portrait_one_col_arabic_template"
#         json_file = f"{base_path}_0_coordinate_fixed.json"
    
#     print(f"Bbox Fine-Tuner")
#     print(f"Input file: {json_file}")
    
#     if not os.path.exists(json_file):
#         print(f"ERROR: File not found")
#         print(f"Usage: python bbox_fine_tuner.py <json_file>")
#         return
    
#     quick_fix_suggestions()
    
#     # Run interactive fine-tuning
#     interactive_fine_tuning(json_file)

# if __name__ == "__main__":
#     main()

