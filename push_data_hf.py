#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from tqdm import tqdm
import logging
from huggingface_hub import HfApi, create_repo, upload_folder
from datasets import Dataset, DatasetDict
import pandas as pd

class HuggingFaceDatasetUploader:
    """
    Uploads JSON document datasets to Hugging Face Hub.
    Handles directory structures and creates proper dataset formats.
    """
    
    def __init__(self, hf_token: Optional[str] = None, log_file: str = "hf_upload.log"):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_file,
            filemode='w'
        )
        self.logger = logging.getLogger()
        
        # Initialize HF API
        self.api = HfApi(token=hf_token)
        self.hf_token = hf_token or os.getenv("HF_TOKEN")
        
        if not self.hf_token:
            raise ValueError("Hugging Face token required. Set HF_TOKEN env var or pass token parameter.")
    
    def load_json_files(self, json_dir: str) -> List[Dict[str, Any]]:
        """Load all JSON files from directory structure."""
        json_path = Path(json_dir)
        all_documents = []
        
        if not json_path.exists():
            raise FileNotFoundError(f"Directory {json_dir} does not exist!")
        
        # Find all JSON files in subdirectories
        json_files = []
        subdirs = [d for d in json_path.iterdir() if d.is_dir()]
        
        print(f"Found {len(subdirs)} book directories...")
        
        for subdir in subdirs:
            book_name = subdir.name
            subdir_files = list(subdir.glob("*.json"))
            json_files.extend([(f, book_name) for f in subdir_files])
            print(f"  {book_name}: {len(subdir_files)} files")
        
        if not json_files:
            print("No JSON files found in subdirectories")
            return []
        
        print(f"\nLoading {len(json_files)} JSON files...")
        
        # Load and process each JSON file
        for json_file, book_name in tqdm(json_files, desc="Loading JSON files"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Create document record
                document = {
                    'id': f"{book_name}_{json_file.stem}",
                    'book_name': book_name,
                    'section_name': json_file.stem,
                    'file_path': str(json_file.relative_to(json_path)),
                    'main_text': data.get('main_text', []),
                    'text': data.get('text', []),
                    'num_elements': len(data.get('main_text', [])),
                    'num_text_refs': len(data.get('text', []))
                }
                
                all_documents.append(document)
                
            except Exception as e:
                self.logger.error(f"Failed to load {json_file}: {e}")
                continue
        
        print(f"Successfully loaded {len(all_documents)} documents")
        return all_documents
    
    def create_dataset_from_documents(self, documents: List[Dict[str, Any]]) -> Dataset:
        """Create Hugging Face Dataset from document list."""
        if not documents:
            raise ValueError("No documents to create dataset from")
        
        # Convert to pandas DataFrame first for easier handling
        df = pd.DataFrame(documents)
        
        # Create dataset
        dataset = Dataset.from_pandas(df)
        
        print(f"Created dataset with {len(dataset)} documents")
        print(f"Dataset features: {list(dataset.features.keys())}")
        
        return dataset
    
    def upload_as_files(self, json_dir: str, repo_id: str, private: bool = False):
        """Upload JSON files directly to HF Hub as files (not dataset)."""
        try:
            # Create repository
            create_repo(
                repo_id=repo_id,
                token=self.hf_token,
                private=private,
                exist_ok=True
            )
            print(f"Repository {repo_id} created/verified")
            
            # Upload entire folder structure
            upload_folder(
                folder_path=json_dir,
                repo_id=repo_id,
                token=self.hf_token,
                commit_message="Upload JSON document dataset"
            )
            
            print(f"✅ Successfully uploaded {json_dir} to {repo_id}")
            self.logger.info(f"Upload complete: {repo_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to upload to {repo_id}: {e}")
            raise
    
    def upload_as_dataset(self, json_dir: str, repo_id: str, private: bool = False, 
                         split_by_book: bool = True):
        """Upload JSON files as a proper Hugging Face Dataset."""
        try:
            # Load documents
            documents = self.load_json_files(json_dir)
            
            if not documents:
                raise ValueError("No documents found to upload")
            
            if split_by_book:
                # Create separate splits for each book
                book_names = list(set(doc['book_name'] for doc in documents))
                dataset_dict = {}
                
                for book_name in book_names:
                    book_docs = [doc for doc in documents if doc['book_name'] == book_name]
                    book_dataset = self.create_dataset_from_documents(book_docs)
                    # Use safe split names (replace special chars)
                    safe_book_name = book_name.replace('-', '_').replace(' ', '_')
                    dataset_dict[safe_book_name] = book_dataset
                
                final_dataset = DatasetDict(dataset_dict)
                print(f"Created DatasetDict with {len(dataset_dict)} splits")
                
            else:
                # Single dataset with all documents
                final_dataset = self.create_dataset_from_documents(documents)
            
            # Push to hub
            final_dataset.push_to_hub(
                repo_id=repo_id,
                token=self.hf_token,
                private=private
            )
            
            print(f"✅ Successfully uploaded dataset to {repo_id}")
            self.logger.info(f"Dataset upload complete: {repo_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to upload dataset to {repo_id}: {e}")
            raise
    
    def create_readme(self, json_dir: str, repo_id: str, dataset_name: str):
        """Create a README.md file for the dataset."""
        documents = self.load_json_files(json_dir)
        
        if not documents:
            return
        
        book_names = list(set(doc['book_name'] for doc in documents))
        total_docs = len(documents)
        total_elements = sum(doc['num_elements'] for doc in documents)
        
        readme_content = f"""# {dataset_name}

## Dataset Description

This dataset contains processed document sections from EPUB books converted to JSON format for synthetic data generation.

## Dataset Statistics

- **Total Documents**: {total_docs:,}
- **Total Books**: {len(book_names)}
- **Total Text Elements**: {total_elements:,}
- **Average Elements per Document**: {total_elements/total_docs:.1f}

## Books Included

{chr(10).join(f'- {book}' for book in sorted(book_names))}

## Dataset Structure

Each document contains:
- `id`: Unique identifier (book_name + section_name)
- `book_name`: Source book name
- `section_name`: Section identifier
- `file_path`: Original file path
- `main_text`: List of main text elements with labels
- `text`: Referenced text content
- `num_elements`: Number of main text elements
- `num_text_refs`: Number of text references

## Usage

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("{repo_id}")

# Access a specific book (if split by book)
book_data = dataset["book_name"]

# Or load as single dataset
# dataset = load_dataset("{repo_id}", split="train")
```

## Data Processing

This dataset was generated from EPUB files through the following pipeline:
1. EPUB → HTML conversion
2. HTML → Docling format conversion  
3. Docling → JSON format conversion
4. Upload to Hugging Face Hub

## License

Please check the original source materials for license information.
"""
        
        readme_path = Path(json_dir) / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"Created README.md at {readme_path}")
        return str(readme_path)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Upload JSON documents to Hugging Face Hub")
    parser.add_argument("json_dir", help="Directory containing JSON files")
    parser.add_argument("repo_id", help="Hugging Face repository ID (username/repo-name)")
    parser.add_argument("--token", help="Hugging Face token (or set HF_TOKEN env var)")
    parser.add_argument("--private", action="store_true", help="Make repository private")
    parser.add_argument("--as-files", action="store_true", help="Upload as files instead of dataset")
    parser.add_argument("--no-split", action="store_true", help="Don't split by book names")
    parser.add_argument("--dataset-name", help="Dataset name for README", default="Document Dataset")
    
    args = parser.parse_args()
    
    try:
        uploader = HuggingFaceDatasetUploader(hf_token=args.token)
        
        # Create README
        uploader.create_readme(args.json_dir, args.repo_id, args.dataset_name)
        
        if args.as_files:
            # Upload as files
            uploader.upload_as_files(args.json_dir, args.repo_id, args.private)
        else:
            # Upload as dataset
            uploader.upload_as_dataset(
                args.json_dir, 
                args.repo_id, 
                args.private,
                split_by_book=not args.no_split
            )
        
        print(f"\n🎉 Dataset available at: https://huggingface.co/datasets/{args.repo_id}")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())