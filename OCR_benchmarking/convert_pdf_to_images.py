import os
from pdf2image import convert_from_path
from pathlib import Path

def convert_pdfs_to_images(input_dir="testing_pdfs", output_dir="testing_images"):
    """
    Convert all PDFs in input_dir to images and save them in output_dir
    
    Args:
        input_dir (str): Directory containing PDF files
        output_dir (str): Directory to save converted images
    """
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Get all PDF files from input directory
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist!")
        return
    
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in '{input_dir}'")
        return
    
    print(f"Found {len(pdf_files)} PDF files to convert...")
    
    for pdf_file in pdf_files:
        try:
            print(f"Converting: {pdf_file.name}")
            
            # Convert PDF to images
            images = convert_from_path(pdf_file)
            
            # Get filename without extension
            base_name = pdf_file.stem
            
            # Save each page as a separate image
            for i, image in enumerate(images):
                # Create output filename
                output_filename = f"{base_name}_image_{i}.png"
                output_path = Path(output_dir) / output_filename
                
                # Save image
                image.save(output_path, "PNG")
                print(f"  Saved: {output_filename}")
            
            print(f"Successfully converted {pdf_file.name} ({len(images)} pages)")
            
        except Exception as e:
            print(f"Error converting {pdf_file.name}: {str(e)}")
    
    print("Conversion complete!")

def main():
    """Main function to run the PDF to image conversion"""
    convert_pdfs_to_images()

if __name__ == "__main__":
    main()