import os
import shutil
from datetime import datetime
from tqdm import tqdm

source_dir = '/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/datasets/html_doc'
target_dir = '/share/users/ahmed_heakl/ymk/OCR/OCR/synthetic_data_generation/datasets/html_doc_3'

# Create the target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Gather all the JSON files in the source directory
json_files = []
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

# Use tqdm for showing progress during the copying process
for source_file in tqdm(json_files, desc="Copying JSON files", unit="file"):
    # Extract the filename and the directory name
    file_name = os.path.basename(source_file)
    dir_name = os.path.basename(os.path.dirname(source_file))

    # Generate a unique file name by appending the directory name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    file_name, file_extension = os.path.splitext(file_name)
    unique_file_name = f"{dir_name}_{file_name}{file_extension}"
    
    # Construct the target file path
    target_file = os.path.join(target_dir, unique_file_name)
    
    # Copy the file to the target directory
    shutil.copy(source_file, target_file)

print("File copying complete.")
