from PIL import Image

from data_loading.data_loader import DataLoader
from synthetic_data_generation.templates.template import Template

class TargetLatexDocumentStore:
    """
    This class provides global accessibility to the latex document that is
    currently being worked with by the SyntheticDataGenerator. Specifically,
    it provides access to the individual pages of that document as PIL images.
    """

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(TargetLatexDocumentStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._target_latex_doc_path = ""
        self._page_images = None

    def init(self, gen_latex_doc_path: str):
        self._page_images = None
        self._target_latex_doc_path = gen_latex_doc_path

    def get_page_image(self, index: int, dpi: int=None) -> Image.Image:
        try:
            if (self._page_images is None):
                self._page_images = self.load_page_images(dpi)
            return self._page_images[index]
        except:
            return None

    def load_page_images(self, dpi: int=None):
        if (dpi is None):
            layout_settings = Template().get_layout_settings()
            size = layout_settings.get_page_size_px()
            return DataLoader().load_doc_page_images(
                self._target_latex_doc_path, size=size)
        return DataLoader().load_doc_page_images(
            self._target_latex_doc_path, dpi=dpi)

    def clear(self):
        self._target_latex_doc_path = ""
        self._page_images = None
