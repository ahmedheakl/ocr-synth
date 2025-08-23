source  /share/users/ahmed_heakl/ymk/OCR/ocr/bin/activate
LOG_ID=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/${LOG_ID}.txt"
python synthetic_data_generator.py -e dev -c "/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/config/config.json" > $LOG_FILE 2>&1
ROOT=/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/generated_latex/internal/13052715_section_024_portrait_one_col_arabic_template
JSON_FILE="${ROOT}_0.json"
POS_FILE="${ROOT}_0.pos"
python fix_pos_v2.py $JSON_FILE $POS_FILE
cd pdf_layout
OUTPUT_FILE="${ROOT}_0_simple_fixed.json"
python draw_bboxes.py  $OUTPUT_FILE
cd ..