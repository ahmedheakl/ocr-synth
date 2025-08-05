import hashlib
from pathlib import Path

def gen_doc_hash(doc_file_path) -> str:
    with Path(doc_file_path).open("rb") as fp:
        hasher = hashlib.sha256()
        block_size = 65536
        buffer = fp.read(block_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = fp.read(block_size)
    return hasher.hexdigest()

def gen_page_hash(doc_hash: str, page_num: int) -> str:
    hasher = hashlib.sha256()
    doc_page_string = f"{doc_hash}:{page_num}"
    hasher.update(doc_page_string.encode("utf-8"))
    return hasher.hexdigest()
