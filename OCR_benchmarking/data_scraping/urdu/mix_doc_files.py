import os
import shutil
from pathlib import Path

source_dir = "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/urdu/html_doc"
dest_dir = "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/urdu/html_doc_mix"

# Create destination directory
os.makedirs(dest_dir, exist_ok=True)

# Move and rename files
for json_file in Path(source_dir).rglob("*.json"):
    subdir_name = json_file.parent.name
    new_name = f"{subdir_name}_{json_file.name}"
    shutil.move(str(json_file), os.path.join(dest_dir, new_name))