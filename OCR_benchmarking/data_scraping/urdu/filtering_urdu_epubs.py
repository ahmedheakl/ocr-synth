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

def clean_epub_directory_single(directory_path):
    """
    Check all EPUB files in a single directory and return statistics
    
    Args:
        directory_path (Path): Path object to directory containing EPUB files
        
    Returns:
        dict: Statistics about the directory processing
    """
    # Find all EPUB files in this directory only (not recursive)
    epub_files = list(directory_path.glob("*.epub")) + list(directory_path.glob("*.EPUB"))
    
    if not epub_files:
        return {
            'directory': directory_path.name,
            'total_files': 0,
            'valid_files': 0,
            'invalid_files': 0,
            'deleted_files': 0,
            'files_to_delete': []
        }
    
    print(f"\n📁 Processing directory: {directory_path.name}")
    print(f"   Found {len(epub_files)} EPUB file(s)")
    
    valid_files = []
    invalid_files = []
    
    # Check each EPUB file
    for epub_file in epub_files:
        print(f"   Checking: {epub_file.name}...", end=" ")
        
        if is_epub_valid(epub_file):
            print("✓ Valid")
            valid_files.append(epub_file)
        else:
            print("✗ Invalid")
            invalid_files.append(epub_file)
    
    return {
        'directory': directory_path.name,
        'total_files': len(epub_files),
        'valid_files': len(valid_files),
        'invalid_files': len(invalid_files),
        'deleted_files': 0,
        'files_to_delete': invalid_files
    }

def clean_epub_directories_nested(root_directory_path, confirm_deletion=True):
    """
    Check all EPUB files in subdirectories and remove invalid ones
    
    Args:
        root_directory_path (str): Path to root directory containing subdirectories with EPUB files
        confirm_deletion (bool): Whether to ask for confirmation before deleting files
    """
    # Convert to Path object for easier handling
    root_path = Path(root_directory_path)
    
    # Check if directory exists
    if not root_path.exists():
        print(f"Error: Directory '{root_directory_path}' does not exist.")
        return
    
    if not root_path.is_dir():
        print(f"Error: '{root_directory_path}' is not a directory.")
        return
    
    # Find all subdirectories
    subdirs = [d for d in root_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"No subdirectories found in '{root_directory_path}'")
        return
    
    print(f"Found {len(subdirs)} subdirectory(ies) to process...")
    
    # Process each subdirectory
    all_stats = []
    total_epub_files = 0
    total_valid_files = 0
    total_invalid_files = 0
    
    for subdir in subdirs:
        stats = clean_epub_directory_single(subdir)
        all_stats.append(stats)
        total_epub_files += stats['total_files']
        total_valid_files += stats['valid_files']
        total_invalid_files += stats['invalid_files']
    
    # Overall summary
    print(f"\n" + "="*50)
    print(f"OVERALL SUMMARY")
    print(f"="*50)
    print(f"Directories processed: {len(subdirs)}")
    print(f"Total EPUB files found: {total_epub_files}")
    print(f"Valid files: {total_valid_files}")
    print(f"Invalid files: {total_invalid_files}")
    
    if total_invalid_files == 0:
        print("\n🎉 All EPUB files are valid! No cleanup needed.")
        return
    
    # Show detailed breakdown
    print(f"\nDETAILED BREAKDOWN:")
    print(f"-" * 30)
    for stats in all_stats:
        if stats['total_files'] > 0:
            print(f"📁 {stats['directory']}: {stats['valid_files']} valid, {stats['invalid_files']} invalid")
    
    # Show all invalid files
    print(f"\nINVALID FILES TO BE REMOVED:")
    print(f"-" * 35)
    all_invalid_files = []
    for stats in all_stats:
        if stats['files_to_delete']:
            print(f"\n📁 {stats['directory']}:")
            for invalid_file in stats['files_to_delete']:
                print(f"   ✗ {invalid_file.name}")
                all_invalid_files.extend(stats['files_to_delete'])
    
    # Confirm deletion
    if confirm_deletion:
        response = input(f"\nDo you want to delete {total_invalid_files} invalid file(s) across all directories? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    # Delete invalid files
    total_deleted = 0
    print(f"\nDELETING INVALID FILES:")
    print(f"-" * 25)
    
    for stats in all_stats:
        if stats['files_to_delete']:
            print(f"\n📁 {stats['directory']}:")
            deleted_count = 0
            for invalid_file in stats['files_to_delete']:
                try:
                    invalid_file.unlink()  # Delete the file
                    print(f"   ✓ Deleted: {invalid_file.name}")
                    deleted_count += 1
                    total_deleted += 1
                except Exception as e:
                    print(f"   ✗ Error deleting {invalid_file.name}: {e}")
            stats['deleted_files'] = deleted_count
    
    # Final summary
    print(f"\n" + "="*50)
    print(f"CLEANUP COMPLETE!")
    print(f"="*50)
    print(f"Total files deleted: {total_deleted}")
    
    # Per-directory deletion summary
    print(f"\nPER-DIRECTORY RESULTS:")
    print(f"-" * 25)
    for stats in all_stats:
        if stats['total_files'] > 0:
            print(f"📁 {stats['directory']}: {stats['deleted_files']} deleted, {stats['valid_files']} remaining")

def main():
    """Main function to run the nested EPUB cleaner"""
    print("Nested EPUB File Validator and Cleaner")
    print("=" * 42)
    print("This tool processes subdirectories containing EPUB files")
    
    # Get directory path from user
    root_path = input("\nEnter the root directory path (containing subdirectories with EPUBs): ").strip()
    
    # Remove quotes if user pasted a quoted path
    root_path = root_path.strip('"\'')
    
    if not root_path:
        print("No directory path provided. Exiting.")
        return
    
    # Run the cleanup
    clean_epub_directories_nested(root_path)

if __name__ == "__main__":
    main()