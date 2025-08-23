from tqdm import tqdm
import subprocess
import os
try:
    from PyPDF2 import PdfReader
except ImportError:
    raise ImportError("PyPDF2 is not installed. Please `pip install PyPDF2` to install it.")
import zipfile
from argparse import ArgumentParser
from multiprocessing import Pool, cpu_count, Manager

request_template = """
curl -s -L -o {output_path} \
  -d "authenticity_token={auth_token}" \
  -d "format={download_format}" \
  -d "commit=הורדה" \
  https://benyehuda.org/download/{book_id}
"""
MAX_ID = 1_000_000
AUTH_TOKEN = "yUmhdy4BUEEalAGYY4RTBQNWcwqqsR6_mp7m3-0CHP3JZrMTqY3AYYURinCi4U6vHdIO3tEyU439ClUBtIVIWA"


def is_pdf_valid(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        for _ in reader.pages:
            pass
        return True
    except Exception:
        return False


def is_epub_valid(path):
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


def download_book(book_id, args):
    output_path = os.path.join(args.output_dir, f"{book_id}.{args.format}")
    if os.path.exists(output_path):
        return False

    cmd = request_template.format(
        output_path=output_path,
        auth_token=AUTH_TOKEN,
        download_format=args.format,
        book_id=book_id,
    )
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        return False

    check_function = is_pdf_valid if args.format == "pdf" else is_epub_valid
    if not check_function(output_path):
        try:
            os.remove(output_path)
        except FileNotFoundError:
            pass
        return False
    return True
def worker_task(book_id_args):
    """Wrapper for multiprocessing (book_id, args)."""
    book_id, args = book_id_args
    return download_book(book_id, args)


def main():
    parser = ArgumentParser(description="Download Hebrew books from Ben Yehuda site.")
    parser.add_argument("--format", choices=["pdf", "epub"], default="epub")
    parser.add_argument("--output_dir", default="benyehuda_epub")
    parser.add_argument("--num_files", type=int, default=1_000_000)
    parser.add_argument("--start_id", type=int, default=1)
    parser.add_argument("--workers", type=int, default=cpu_count())
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with Pool(processes=args.workers) as pool:
        results = []
        with tqdm(total=args.num_files) as pbar:
            # pack (book_id, args) since pool.map only takes one argument
            task_iter = ((bid, args) for bid in range(args.start_id, MAX_ID))
            for ok in pool.imap_unordered(worker_task, task_iter):
                if ok:
                    results.append(ok)
                    pbar.update(1)
                if len(results) >= args.num_files:
                    pool.terminate()
                    break


if __name__ == "__main__":
    main()
