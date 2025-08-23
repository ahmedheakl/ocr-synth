import json
import os
from internetarchive import get_item
from tqdm import tqdm

# Create download directory
download_dir = "downloaded_epubs"
os.makedirs(download_dir, exist_ok=True)

# Read identifiers
with open("/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/persian/identifiers.json", 'r', encoding='utf-8') as file:
    ids = json.load(file)

print(f"Found {len(ids)} identifiers to process")
print(f"Downloads will be saved to: {os.path.abspath(download_dir)}")

# Track statistics
downloaded_count = 0
epub_not_available_count = 0
error_count = 0

# Process each identifier with progress bar
for file_id in tqdm(ids, desc="Processing items", unit="item"):
    try:
        item = get_item(file_id)
        
        if not item.exists:
            tqdm.write(f"Item {file_id} does not exist")
            error_count += 1
            continue
        
        # Get available formats from files
        formats = set()
        for file_obj in item.files:
            if 'format' in file_obj:
                formats.add(file_obj['format'])
        
        # Check if EPUB is available
        if "EPUB" in formats:
            tqdm.write(f"Downloading EPUB for {file_id}")
            # Download to specific directory
            item.download(
                formats=['EPUB'], 
                destdir=download_dir,
                verbose=False,
                ignore_existing=True  # Skip if already downloaded
            )
            downloaded_count += 1
        else:
            epub_not_available_count += 1
            tqdm.write(f"EPUB not available for {file_id}. Available formats: {list(formats)}")
            
    except Exception as e:
        error_count += 1
        tqdm.write(f"Error processing {file_id}: {str(e)}")

# Print summary
print(f"\n--- Download Summary ---")
print(f"Total items processed: {len(ids)}")
print(f"Successfully downloaded: {downloaded_count}")
print(f"EPUB not available: {epub_not_available_count}")
print(f"Errors encountered: {error_count}")
print(f"Downloads saved to: {os.path.abspath(download_dir)}")