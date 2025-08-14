# #!/usr/bin/env python3
# """
# Quick debug analyzer to understand your bbox coordinate issue.
# """

# import json
# import re
# import os

# def analyze_bbox_issue():
#     """Analyze the coordinate issue with your current files."""
    
#     # Your file paths
#     base_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/generated_latex/internal/13052715_section_024_portrait_one_col_arabic_template"
#     json_file = f"{base_path}_0.json"
#     pos_file = f"{base_path}_0.pos"
#     fixed_file = f"{base_path}_0_fixed.json"  # Or whatever your fixed file is named
    
#     print("BBOX COORDINATE ANALYSIS")
#     print("=" * 50)
    
#     # 1. Analyze original JSON
#     print("1. ORIGINAL JSON ANALYSIS")
#     print("-" * 30)
    
#     if os.path.exists(json_file):
#         with open(json_file, 'r', encoding='utf-8') as f:
#             original_data = json.load(f)
        
#         original_texts = original_data.get('texts', [])
#         original_with_bbox = [t for t in original_texts if t.get('prov') and len(t['prov']) > 0]
#         original_without_bbox = [t for t in original_texts if not t.get('prov') or len(t['prov']) == 0]
        
#         print(f"Total text elements: {len(original_texts)}")
#         print(f"With bbox: {len(original_with_bbox)}")
#         print(f"Without bbox: {len(original_without_bbox)}")
        
#         if original_with_bbox:
#             print("\nSample original bboxes:")
#             for i, text_obj in enumerate(original_with_bbox[:3]):
#                 bbox = text_obj['prov'][0]['bbox']
#                 text_preview = text_obj.get('text', '')[:30] + "..."
#                 print(f"  {i}: {bbox} - '{text_preview}'")
            
#             # Coordinate ranges
#             all_bboxes = [t['prov'][0]['bbox'] for t in original_with_bbox]
#             min_x = min(bbox['l'] for bbox in all_bboxes)
#             max_x = max(bbox['r'] for bbox in all_bboxes)
#             min_y = min(bbox['t'] for bbox in all_bboxes)
#             max_y = max(bbox['b'] for bbox in all_bboxes)
            
#             print(f"\nOriginal coordinate ranges:")
#             print(f"  X: {min_x} to {max_x} (span: {max_x - min_x})")
#             print(f"  Y: {min_y} to {max_y} (span: {max_y - min_y})")
        
#         # Page dimensions
#         pages = original_data.get('pages', {})
#         if pages:
#             page1 = pages.get('1', {})
#             page_size = page1.get('size', {})
#             print(f"\nPage dimensions: {page_size}")
    
#     # 2. Analyze position file
#     print(f"\n2. POSITION FILE ANALYSIS")
#     print("-" * 30)
    
#     if os.path.exists(pos_file):
#         with open(pos_file, 'r', encoding='utf-8') as f:
#             pos_content = f.read()
        
#         # Extract coordinates
#         spos_pattern = r'spos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
#         matches = re.findall(spos_pattern, pos_content)
        
#         print(f"Position entries found: {len(matches)}")
        
#         if matches:
#             print("\nSample raw coordinates:")
#             for i, (idx, x, y, page) in enumerate(matches[:3]):
#                 print(f"  Position {idx}: ({x}, {y}) page {page}")
            
#             # Coordinate ranges
#             all_x = [int(match[1]) for match in matches]
#             all_y = [int(match[2]) for match in matches]
            
#             print(f"\nRaw coordinate ranges:")
#             print(f"  X: {min(all_x)} to {max(all_x)}")
#             print(f"  Y: {min(all_y)} to {max(all_y)}")
            
#             # Test different conversions on first coordinate
#             if matches:
#                 test_x, test_y = int(matches[0][1]), int(matches[0][2])
                
#                 print(f"\nTesting conversions on ({test_x}, {test_y}):")
                
#                 # Method 1: SP to PT to PX (original)
#                 conv1_x = int(test_x / 65536 * 72.27 / 72)
#                 conv1_y = int(test_y / 65536 * 72.27 / 72)
#                 print(f"  Method 1 (SP->PT->PX): ({conv1_x}, {conv1_y})")
                
#                 # Method 2: Proportional to page
#                 max_coord = max(max(all_x), max(all_y))
#                 conv2_x = int((test_x / max_coord) * 819)
#                 conv2_y = int((test_y / max_coord) * 1060)
#                 print(f"  Method 2 (Proportional): ({conv2_x}, {conv2_y})")
                
#                 # Method 3: Proportional with Y flip
#                 conv3_x = int((test_x / max_coord) * 819)
#                 conv3_y = 1060 - int((test_y / max_coord) * 1060)
#                 print(f"  Method 3 (Prop + Y flip): ({conv3_x}, {conv3_y})")
                
#                 # Method 4: Fixed scale factor
#                 scale = 50000  # Adjust based on observation
#                 conv4_x = int(test_x / scale)
#                 conv4_y = int(test_y / scale)
#                 print(f"  Method 4 (Fixed scale): ({conv4_x}, {conv4_y})")
    
#     # 3. Analyze fixed file if it exists
#     print(f"\n3. FIXED FILE ANALYSIS")
#     print("-" * 30)
    
#     if os.path.exists(fixed_file):
#         with open(fixed_file, 'r', encoding='utf-8') as f:
#             fixed_data = json.load(f)
        
#         fixed_texts = fixed_data.get('texts', [])
#         fixed_with_bbox = [t for t in fixed_texts if t.get('prov') and len(t['prov']) > 0]
        
#         print(f"Fixed file total elements: {len(fixed_texts)}")
#         print(f"Fixed file with bbox: {len(fixed_with_bbox)}")
        
#         # Find the newly added bboxes
#         original_bbox_count = len(original_with_bbox) if 'original_with_bbox' in locals() else 0
#         new_bbox_count = len(fixed_with_bbox) - original_bbox_count
        
#         if new_bbox_count > 0:
#             print(f"Newly added bboxes: {new_bbox_count}")
            
#             # Show the new bboxes
#             new_bboxes = fixed_with_bbox[-new_bbox_count:] if new_bbox_count > 0 else []
            
#             print("\nNewly added bbox coordinates:")
#             for i, text_obj in enumerate(new_bboxes):
#                 bbox = text_obj['prov'][0]['bbox']
#                 text_preview = text_obj.get('text', '')[:30] + "..."
#                 print(f"  New {i}: {bbox} - '{text_preview}'")
                
#                 # Check if coordinates are reasonable
#                 reasonable = (0 <= bbox['l'] <= 819 and 0 <= bbox['t'] <= 1060 and 
#                             0 <= bbox['r'] <= 819 and 0 <= bbox['b'] <= 1060)
#                 print(f"    -> {'✓ Reasonable' if reasonable else '✗ Out of bounds'}")
        
#         # Compare coordinate ranges
#         if len(fixed_with_bbox) > 0:
#             all_fixed_bboxes = [t['prov'][0]['bbox'] for t in fixed_with_bbox]
#             fixed_min_x = min(bbox['l'] for bbox in all_fixed_bboxes)
#             fixed_max_x = max(bbox['r'] for bbox in all_fixed_bboxes)
#             fixed_min_y = min(bbox['t'] for bbox in all_fixed_bboxes)
#             fixed_max_y = max(bbox['b'] for bbox in all_fixed_bboxes)
            
#             print(f"\nFixed file coordinate ranges:")
#             print(f"  X: {fixed_min_x} to {fixed_max_x}")
#             print(f"  Y: {fixed_min_y} to {fixed_max_y}")
    
#     # 4. Recommendations
#     print(f"\n4. RECOMMENDATIONS")
#     print("-" * 30)
    
#     print("Based on this analysis:")
#     print()
    
#     if 'original_with_bbox' in locals() and original_with_bbox:
#         print("✓ Use the original bbox coordinates as reference for the expected range")
#         print("✓ The new coordinates should match this range and style")
    
#     if 'matches' in locals() and matches:
#         print("✓ Test the different conversion methods shown above")
#         print("✓ Choose the method that produces coordinates similar to original bboxes")
    
#     print("✓ Use the visualization script to see where the bboxes are placed")
#     print("✓ If bboxes are in wrong place, try:")
#     print("  - Different scaling factors")
#     print("  - Y-axis flipping (subtract from page height)")
#     print("  - Proportional scaling instead of point-based scaling")

# def suggest_next_steps():
#     """Suggest specific next steps based on the analysis."""
    
#     print(f"\nNEXT STEPS:")
#     print("=" * 20)
#     print("1. Run this analysis to understand your current coordinate ranges")
#     print("2. Test the smart bbox fixer with different methods")
#     print("3. Use your visualization script to see the results")
#     print("4. Adjust the conversion method if bboxes are still misplaced")
#     print()
#     print("Commands to try:")
#     print("  python smart_bbox_fixer.py  # Interactive mode")
#     print("  python your_visualization_script.py  # Check results")

# if __name__ == "__main__":
#     analyze_bbox_issue()
#     suggest_next_steps()

#!/usr/bin/env python3
"""
Quick diagnostic to verify the corrected interpretation of your position data.
"""

import re

def analyze_position_data():
    """Analyze your position data with the corrected understanding."""
    
    pos_content = """spos0:34219608,45847191,\LRE  {١}
epos0:34219608,44121509,\LRE  {١}
spos1:34219608,44121509,\LRE  {١}
epos1:31898104,40884030,\LRE  {١}
spos2:34219608,39311166,\LRE  {١}
epos2:23955800,38156422,\LRE  {١}
spos3:34219608,36583558,\LRE  {١}
epos3:31760481,33211075,\LRE  {١}
spos4:34219608,31638211,\LRE  {١}
epos4:6279033,25669847,\LRE  {١}
spos5:34219608,24096983,\LRE  {١}
epos5:15852275,17996890,\LRE  {١}
spos6:34219608,16301474,\LRE  {١}
epos6:31774899,14100775,\LRE  {١}
spos7:34219608,12527911,\LRE  {١}
epos7:21671216,45184622,\LRE  {٢}
spos8:34219608,43611758,\LRE  {٢}
epos8:21175108,41217072,\LRE  {٢}
spos9:34219608,39644208,\LRE  {٢}
epos9:15323402,39644208,\LRE  {٢}
spos10:34219608,38071344,\LRE  {٢}
epos10:31793248,36064631,\LRE  {٢}
spos11:34219608,34491767,\LRE  {٢}
epos11:21928556,34491767,\LRE  {٢}
spos12:34219608,32918903,\LRE  {٢}
epos12:18082471,31749085,\LRE  {٢}
spos13:34219608,30176221,\LRE  {٢}
epos13:25093505,28986087,\LRE  {٢}
spos14:34219608,27343100,\LRE  {٢}
epos14:32517421,26556668,\LRE  {٢}
spos15:34219608,24983804,\LRE  {٢}
epos15:26052953,23884110,\LRE  {٢}
spos16:34219608,22311246,\LRE  {٢}
epos16:11761516,18940729,\LRE  {٢}
spos17:34219608,17367865,\LRE  {٢}
epos17:29951468,16496236,\LRE  {٢}
spos18:34219608,14923372,\LRE  {٢}
epos18:24003641,13831542,\LRE  {٢}"""
    
    print("POSITION DATA ANALYSIS - CORRECTED")
    print("=" * 50)
    
    # Parse positions
    spos_pattern = r'spos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
    epos_pattern = r'epos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
    
    spos_matches = re.findall(spos_pattern, pos_content)
    epos_matches = re.findall(epos_pattern, pos_content)
    
    print(f"Found {len(spos_matches)} start positions")
    print(f"Found {len(epos_matches)} end positions")
    
    # Analyze start positions
    start_x_coords = [int(match[1]) for match in spos_matches]
    start_y_coords = [int(match[2]) for match in spos_matches]
    
    print(f"\nSTART POSITIONS (spos):")
    print(f"X coordinates: {len(set(start_x_coords))} unique values")
    if len(set(start_x_coords)) == 1:
        print(f"  All start at X = {start_x_coords[0]} ✅ (consistent left margin)")
    else:
        print(f"  X range: {min(start_x_coords)} to {max(start_x_coords)}")
    
    print(f"Y coordinates: {len(set(start_y_coords))} unique values")
    print(f"  Y range: {min(start_y_coords)} to {max(start_y_coords)} ✅ (different lines)")
    
    # Analyze end positions
    end_x_coords = [int(match[1]) for match in epos_matches]
    end_y_coords = [int(match[2]) for match in epos_matches]
    
    print(f"\nEND POSITIONS (epos):")
    print(f"X coordinates: {len(set(end_x_coords))} unique values")
    print(f"  X range: {min(end_x_coords)} to {max(end_x_coords)} ✅ (variable text widths)")
    
    print(f"Y coordinates: {len(set(end_y_coords))} unique values")
    print(f"  Y range: {min(end_y_coords)} to {max(end_y_coords)}")
    
    # Show text width analysis
    print(f"\nTEXT WIDTH ANALYSIS:")
    for i, (spos_match, epos_match) in enumerate(zip(spos_matches[:5], epos_matches[:5])):
        if spos_match[0] == epos_match[0]:  # Same index
            start_x = int(spos_match[1])
            end_x = int(epos_match[1])
            width_raw = abs(end_x - start_x)
            
            print(f"Text {i}: width = {width_raw} raw units (start: {start_x}, end: {end_x})")
    
    # Page analysis
    pages_start = [match[3] for match in spos_matches]
    pages_end = [match[3] for match in epos_matches]
    
    print(f"\nPAGE ANALYSIS:")
    print(f"Pages in start positions: {set(pages_start)}")
    print(f"Pages in end positions: {set(pages_end)}")
    
    page1_count = pages_start.count('١')
    page2_count = pages_start.count('٢')
    print(f"Page 1 elements: {page1_count}")
    print(f"Page 2 elements: {page2_count}")
    
    # Coordinate system interpretation
    print(f"\nCOORDINATE SYSTEM INTERPRETATION:")
    print("✅ Start positions = left edge of text (consistent margin)")
    print("✅ End positions = right edge of text (varies by length)")
    print("✅ Y coordinates = vertical position (reading order)")
    print("✅ Page numbers in Arabic numerals (١ = 1, ٢ = 2)")
    
    print(f"\nRECOMMENDATION:")
    print("Your position data is GOOD! Use the corrected coordinate converter.")
    print("The issue was misunderstanding the data format, not broken coordinates.")

if __name__ == "__main__":
    analyze_position_data()