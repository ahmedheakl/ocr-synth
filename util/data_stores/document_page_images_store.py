from PIL import Image

from util import file_path_manager

class DocumentPageImagesStore:
    """
    Stores the pages of the origin document that is used for data synthesis as
    page images. Thereby, providing global access to the origin page images.
    """

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(DocumentPageImagesStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._data = None
        self._doc_file_path = None

    def set_data(self, data: list[Image.Image], doc_file_path: str):
        self._data = data
        self._doc_file_path = doc_file_path

    def get_doc_file_path(self) -> str:
        return self._doc_file_path

    def get_doc_file_name(self) -> str:
        return file_path_manager.extract_fname_with_ext(self._doc_file_path)

    def get_doc_file_name_wo_ext(self) -> str:
        return file_path_manager.extract_fname_wo_ext(self._doc_file_path)

    def get_page_images(self) -> list[Image.Image]:
        return self._data
    
    def get_page_image(self, index: int) -> Image.Image:
        return self._data[index]

    def get_page_size(self) -> tuple[int, int]:
        return (self._data[0].width, self._data[0].height)

    def get_page_width_px(self) -> int:
        return self._data[0].width

    def get_page_height_px(self) -> int:
        return self._data[0].height

    def clear(self):
        self._data = None
        self._doc_file_path = None
