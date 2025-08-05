from data_loading.data_loader import DataLoader
from synthetic_data_generation.data_stores.main_text_item_store import MainTextItemStore
from synthetic_data_generation.data_stores.target_latex_document_store import TargetLatexDocumentStore
from synthetic_data_generation.data_stores.wrap_items_store import WrapItemsStore
from synthetic_data_generation.data_structures.latex_document.page_heading_store import PageHeadingStore
from util import file_path_manager
from util.data_stores.ccs_data_store import CcsDataStore
from util.data_stores.docling_data_store import DoclingDataStore
from util.data_stores.document_page_images_store import DocumentPageImagesStore

class DataStoresManager:

    def __init__(self):
        self._docling_data_store = DoclingDataStore()
        self._main_text_item_store = MainTextItemStore()
        self._page_heading_store = PageHeadingStore()
        self._wrap_items_store = WrapItemsStore()
        self._document_page_images_store = DocumentPageImagesStore()
        self._target_latex_doc_store = TargetLatexDocumentStore()

    def init_doc_data_stores(self, file_path: str):
        # self._init_ccs_data_store(file_path)
        self._init_docling_data_store(file_path)
        # self._init_doc_pages_data_store(file_path)

    # def _init_ccs_data_store(self, file_path: str):
    #     ccs_data = DataLoader().load_json_data(file_path)
    #     self._ccs_data_store.set_data(ccs_data)

    def _init_docling_data_store(self, file_path: str):
        docling_data = DataLoader().load_json_data(file_path)
        self._docling_data_store.set_data(docling_data)

    # def _init_doc_pages_data_store(self, file_path: str):
    #     dir_path = file_path_manager.extract_dir_path(file_path)
    #     file_name = file_path_manager.extract_fname_wo_ext(file_path) + ".pdf"
    #     doc_path = dir_path + file_name
    #     images = DataLoader().load_doc_page_images(doc_path)
    #     self._document_page_images_store.set_data(images, doc_path)

    def init_gen_latex_doc_data_store(self, file_path: str):
        self._target_latex_doc_store.init(file_path)

    def clear_data_stores(self):
        self._docling_data_store.clear()
        self._main_text_item_store.clear()
        self._page_heading_store.clear()
        self._wrap_items_store.clear()
        self._document_page_images_store.clear()
        self._target_latex_doc_store.clear()
