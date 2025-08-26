## create env

```bash
python -m venv scraper
```
## activate env 
```bash
source scraper/bin/activate
```

### scraoing hebrew data

```bash
cd hebrew
``

```bash
python scraping_hebrew.py
```

```bash
mkdir -p /share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/hebrew/html_doc_mixed_2 && find /share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/hebrew/html_doc_2 -name "*.json" -type f -exec sh -c 'mv "$1" "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/hebrew/html_doc_mixed_2/$(basename $(dirname "$1"))_$(basename "$1")"' _ {} \;
```

```bash
mkdir -p /share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/persian/html_docs_mixed && find /share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/persian/html_doc_2 -name "*.json" -type f -exec sh -c 'mv "$1" "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/data_scraping/persian/html_docs_mixed/$(basename $(dirname "$1"))_$(basename "$1")"' _ {} \;
```