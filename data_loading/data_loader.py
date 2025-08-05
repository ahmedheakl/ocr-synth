import json
from pdf2image import convert_from_path
from PIL import Image

class DataLoader:

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def load_doc_page_images(
        self, file_path: str, dpi: int=72, size: int=None
    ) -> list[Image.Image]:
        print(f'convert from path doc to images {file_path}')
        if (size is None):
            return convert_from_path(file_path, dpi=dpi)
        return convert_from_path(file_path, size=size)

    def load_json_data(self, file_path: str) -> dict:
        file = open(file_path, encoding="utf-8")
        data = json.load(file)
        file.close()
        return data

    def load_file_as_lines(self, file_path):
        file = open(file_path, "r")
        data = file.readlines()
        file.close()
        return data

    def clean_dir_path(self, dir_path: str) -> str:
        if (dir_path == ""):
            return dir_path
        if (dir_path[-1] == "/"):
            return dir_path
        return dir_path + "/"
