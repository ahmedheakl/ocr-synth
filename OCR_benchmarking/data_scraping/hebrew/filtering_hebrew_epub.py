import os
import zipfile
import glob
from pathlib import Path

def is_epub_valid(path):
    """Check if an EPUB file is valid"""
    try:
        with zipfile.ZipFile(path, "r") as zf:
            if "mimetype" not in zf.namelist():
                return False
            with zf.open("mimetype") as f:
                if f.read().decode("utf-8").strip() != "application/epub+zip":
                    return False
            if "META-INF/container.xml" not in zf.namelist():
                return False
            for name in zf.namelist():
                with zf.open(name) as f:
                    f.read(1024) 
            bad_file = zf.testzip()
            if bad_file is not None:
                return False

        return True
    except Exception:
        return False

def clean_epub_directory(directory_path, confirm_deletion=True):
    """
    Check all EPUB files in a directory and remove invalid ones
    
    Args:
        directory_path (str): Path to directory containing EPUB files
        confirm_deletion (bool): Whether to ask for confirmation before deleting files
    """
    # Convert to Path object for easier handling
    dir_path = Path(directory_path)
    
    # Check if directory exists
    if not dir_path.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    if not dir_path.is_dir():
        print(f"Error: '{directory_path}' is not a directory.")
        return
    
    # Find all EPUB files
    epub_files = list(dir_path.glob("*.epub")) + list(dir_path.glob("*.EPUB"))
    
    if not epub_files:
        print(f"No EPUB files found in '{directory_path}'")
        return
    
    print(f"Found {len(epub_files)} EPUB file(s) to check...")
    
    valid_files = []
    invalid_files = []
    
    # Check each EPUB file
    for epub_file in epub_files:
        print(f"Checking: {epub_file.name}...", end=" ")
        
        if is_epub_valid(epub_file):
            print("✓ Valid")
            valid_files.append(epub_file)
        else:
            print("✗ Invalid")
            invalid_files.append(epub_file)
    
    # Summary
    print(f"\nSummary:")
    print(f"Valid files: {len(valid_files)}")
    print(f"Invalid files: {len(invalid_files)}")
    
    if not invalid_files:
        print("All EPUB files are valid! No cleanup needed.")
        return
    
    # Show invalid files
    print(f"\nInvalid files to be removed:")
    for invalid_file in invalid_files:
        print(f"  - {invalid_file.name}")
    
    # Confirm deletion
    if confirm_deletion:
        response = input(f"\nDo you want to delete {len(invalid_files)} invalid file(s)? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    # Delete invalid files
    deleted_count = 0
    for invalid_file in invalid_files:
        try:
            invalid_file.unlink()  # Delete the file
            print(f"Deleted: {invalid_file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {invalid_file.name}: {e}")
    
    print(f"\nCleanup complete! Deleted {deleted_count} invalid EPUB file(s).")

def main():
    """Main function to run the EPUB cleaner"""
    print("EPUB File Validator and Cleaner")
    print("=" * 35)
    
    # Get directory path from user
    dir_path = input("Enter the directory path containing EPUB files: ").strip()
    
    # Remove quotes if user pasted a quoted path
    dir_path = dir_path.strip('"\'')
    
    if not dir_path:
        print("No directory path provided. Exiting.")
        return
    
    # Run the cleanup
    clean_epub_directory(dir_path)

if __name__ == "__main__":
    main()