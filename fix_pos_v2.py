import json
import re
import os
import sys
from typing import Dict, List, Tuple

def convert_arabic_numerals(arabic_num: str) -> str:
    arabic_to_western = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    western_num = ""
    for char in arabic_num:
        western_num += arabic_to_western.get(char, char)
    return western_num

def parse_position_file_simple(pos_file_path: str) -> List[Dict]:
    positions = []
    with open(pos_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    spos_pattern = r'spos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
    epos_pattern = r'epos(\d+):(\d+),(\d+),\\LRE\s*\{([^}]+)\}'
    spos_matches = re.findall(spos_pattern, content)
    epos_matches = re.findall(epos_pattern, content)
    print(f"Found {len(spos_matches)} start positions and {len(epos_matches)} end positions")
    for spos_match in spos_matches:
        index, sx, sy, spage = spos_match
        index = int(index)
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
    positions.sort(key=lambda x: x['index'])
    return positions

def analyze_existing_bboxes(json_data: dict) -> Dict:
    texts = json_data.get('texts', [])
    existing_bboxes = []
    for text_obj in texts:
        if text_obj.get('prov') and len(text_obj['prov']) > 0:
            bbox = text_obj['prov'][0].get('bbox')
            if bbox and isinstance(bbox, dict):
                existing_bboxes.append({
                    'l': bbox['l'], 't': bbox['t'], 'r': bbox['r'], 'b': bbox['b'],
                    'width': bbox['r'] - bbox['l'],
                    'height': bbox['b'] - bbox['t']
                })
    
    if not existing_bboxes:
        print("No existing bboxes found for analysis")
        return {'count': 0}
    analysis = {
        'count': len(existing_bboxes),
        'avg_left': sum(b['l'] for b in existing_bboxes) / len(existing_bboxes),
        'avg_top': sum(b['t'] for b in existing_bboxes) / len(existing_bboxes),
        'avg_width': sum(b['width'] for b in existing_bboxes) / len(existing_bboxes),
        'avg_height': sum(b['height'] for b in existing_bboxes) / len(existing_bboxes),
        'min_top': min(b['t'] for b in existing_bboxes),
        'max_bottom': max(b['b'] for b in existing_bboxes),
        'left_margin': min(b['l'] for b in existing_bboxes),
        'right_margin': max(b['r'] for b in existing_bboxes),
    }
    print(f"Existing bbox analysis:")
    print(f"  Count: {analysis['count']}")
    print(f"  Average position: ({analysis['avg_left']:.1f}, {analysis['avg_top']:.1f})")
    print(f"  Average size: {analysis['avg_width']:.1f} x {analysis['avg_height']:.1f}")
    print(f"  Y range: {analysis['min_top']:.1f} to {analysis['max_bottom']:.1f}")
    print(f"  X range: {analysis['left_margin']:.1f} to {analysis['right_margin']:.1f}")
    return analysis

def convert_coordinates_simple(raw_x: int, raw_y: int, conversion_factors: dict) -> Tuple[int, int]:
    scale_factor = conversion_factors.get('scale_factor', 1.0 / 49152)  # Empirically determined
    x_px = int(raw_x * scale_factor)
    y_px = int(raw_y * scale_factor)
    x_offset = conversion_factors.get('x_offset', 0)
    y_offset = conversion_factors.get('y_offset', 0)
    final_x = x_px + x_offset
    final_y = y_px + y_offset
    final_x = max(0, min(final_x, 819))
    final_y = max(0, min(final_y, 1060))
    return final_x, final_y

def calculate_conversion_factors(existing_analysis: dict, pos_data: List[dict]) -> dict:
    if existing_analysis['count'] == 0 or not pos_data:
        return {
            'scale_factor': 1.0 / 49152,
            'x_offset': 50,
            'y_offset': 50
        }
    target_left_margin = existing_analysis['left_margin']
    target_top_start = existing_analysis['min_top']
    if pos_data:
        pos_x_range = max(p['start_x'] for p in pos_data) - min(p['start_x'] for p in pos_data)
        pos_y_range = max(p['start_y'] for p in pos_data) - min(p['start_y'] for p in pos_data)
        
        existing_x_range = existing_analysis['right_margin'] - existing_analysis['left_margin']
        existing_y_range = existing_analysis['max_bottom'] - existing_analysis['min_top']
        if pos_x_range > 0 and existing_x_range > 0:
            x_scale = existing_x_range / pos_x_range
            scale_factor = x_scale
        else:
            scale_factor = 1.0 / 49152
        if pos_data:
            min_pos_x = min(p['start_x'] for p in pos_data)
            min_pos_y = min(p['start_y'] for p in pos_data)
            x_offset = target_left_margin - (min_pos_x * scale_factor)
            y_offset = target_top_start - (min_pos_y * scale_factor)
        else:
            x_offset = target_left_margin
            y_offset = target_top_start
    else:
        scale_factor = 1.0 / 49152
        x_offset = target_left_margin
        y_offset = target_top_start
    
    return {
        'scale_factor': scale_factor,
        'x_offset': x_offset,
        'y_offset': y_offset
    }

def fix_missing_bboxes(json_file_path: str, pos_file_path: str) -> str:
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            doc_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None
    
    # Parse position data
    pos_data = parse_position_file_simple(pos_file_path)
    if not pos_data:
        print("No position data found")
        return None
    
    print(f"Parsed {len(pos_data)} position entries")
    
    # Analyze existing coordinates
    existing_analysis = analyze_existing_bboxes(doc_data)
    
    # Calculate conversion factors
    conversion_factors = calculate_conversion_factors(existing_analysis, pos_data)
    print(f"Conversion factors: {conversion_factors}")
    
    # Fix missing bboxes
    texts = doc_data.get('texts', [])
    fixed_count = 0
    
    print(f"\nProcessing {len(texts)} text elements...")
    
    for i, text_obj in enumerate(texts):
        # Check if bbox data is missing
        if not text_obj.get('prov') or len(text_obj['prov']) == 0:
            if i < len(pos_data):
                pos_item = pos_data[i]
                
                # Convert coordinates using simple conversion
                start_x, start_y = convert_coordinates_simple(
                    pos_item['start_x'], pos_item['start_y'], conversion_factors
                )
                end_x, end_y = convert_coordinates_simple(
                    pos_item['end_x'], pos_item['end_y'], conversion_factors
                )
                
                # Create bbox
                left = min(start_x, end_x)
                right = max(start_x, end_x)
                top = min(start_y, end_y)
                bottom = max(start_y, end_y)
                
                # Ensure minimum reasonable dimensions
                if right - left < 10:
                    right = left + 100
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
                text_preview = text_obj.get('text', '')[:30] + "..."
                print(f"✓ Fixed element {i}: {bbox} - '{text_preview}'")
    
    print(f"\nFixed {fixed_count} text elements")
    
    # Save fixed file
    fixed_file_path = json_file_path.replace('.json', '_simple_fixed.json')
    
    try:
        with open(fixed_file_path, 'w', encoding='utf-8') as f:
            json.dump(doc_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved fixed file: {fixed_file_path}")
        return fixed_file_path
        
    except Exception as e:
        print(f"Error saving fixed file: {e}")
        return None

def main():
    """Main function."""
    
    if len(sys.argv) < 3:
        # Use default paths if no arguments provided
        base_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/generated_latex/internal/13052715_section_024_portrait_one_col_arabic_template"
        json_file = f"{base_path}_0.json"
        pos_file = f"{base_path}_0.pos"
    else:
        json_file = sys.argv[1]
        pos_file = sys.argv[2]
    
    print("Simple Arabic Bbox Fixer")
    print("=" * 40)
    
    # Check if files exist
    if not os.path.exists(json_file):
        print(f"ERROR: JSON file not found: {json_file}")
        return
    
    if not os.path.exists(pos_file):
        print(f"ERROR: Position file not found: {pos_file}")
        return
    
    # Fix the file
    fixed_file = fix_missing_bboxes(json_file, pos_file)
    
    if fixed_file:
        print(f"\n✅ SUCCESS!")
        print(f"Fixed file: {fixed_file}")
        print(f"Test this with your visualization script to check the results.")
    else:
        print("❌ FAILED")

if __name__ == "__main__":
    main()