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

