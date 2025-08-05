from PIL import Image

from synthetic_data_generation.config.config import Config
from synthetic_data_generation.config.export_data_keys import ExportDataKeys
from synthetic_data_generation.util.unit_converter import UnitConverter
from util.data_stores.document_page_images_store import DocumentPageImagesStore
from util import document_hasher
from .segment import Segment

class PageExportData:

    def __init__(self, synth_doc_name: str, page_num: str):
        self._synth_doc_name = synth_doc_name
        print(f'saving for page number {page_num}')
        self._page_num = page_num
        self._page_image = None
        self._cells = []
        self._segments = []
        self._doc_hash = None
        self._page_hash = None

    def get_page_num(self) -> int:
        return self._page_num

    def get_page_image(self) -> Image.Image:
        return self._page_image

    def get_last_segment(self) -> Segment:
        try:
            return self._segments[-1]
        except:
            return None

    def add_cell(self, cell):
        self._cells.append(cell)

    def add_segment(self, segment: Segment):
        self._segments.append(segment)

    def add_page_image(self, page_image: Image.Image):
        self._page_image = page_image

    def add_doc_and_page_hashes(self, doc_hash: str):
        self._doc_hash = doc_hash
        self._page_hash = document_hasher.gen_page_hash(
            self._doc_hash, self._page_num)

    def to_dict(self) -> dict:
        data = {
            ExportDataKeys.SYNTH_DOC_NAME: self._synth_doc_name,
            ExportDataKeys.EXTRA_PAGE_NUM: self._page_num,
            ExportDataKeys.DOC_HASH: self._doc_hash,
            ExportDataKeys.PAGE_HASH: self._page_hash,
            ExportDataKeys.EXTRA_HEIGHT_PT: int(
                UnitConverter().px_to_pt(self._page_image.height)),
            ExportDataKeys.EXTRA_WIDTH_PT: int(
                UnitConverter().px_to_pt(self._page_image.width)),
            ExportDataKeys.CELLS: [cell.to_dict() for cell in self._cells],
            ExportDataKeys.SEGMENTS: [segm.to_dict() for segm in self._segments]
        }
        data.update(Config().get_export_data_config().get_config_data())
        return data

    def print(self):
        for key, value in self.to_dict().items():
            print(key, ": ", value)
        print("========================================")
