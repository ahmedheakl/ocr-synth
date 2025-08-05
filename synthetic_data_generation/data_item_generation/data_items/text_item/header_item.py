from pylatex import Head

from synthetic_data_generation.data_structures.latex_document.page_heading_store import PageHeadingStore
from util.retrieve_index_from_reference import retrieve_index_from_reference
from util.data_stores.ccs_data_store import CcsDataStore
from util.data_stores.docling_data_store import DoclingDataStore
from .heading_item import HeadingItem

class HeaderItem(HeadingItem):

    def __init__(self, index, data: dict):
        page_header_data = self._get_page_header_data(data)
        super().__init__(index, page_header_data)

    def add_as_latex_to_doc(self, doc):
        page_heading = PageHeadingStore().get_page_heading(self._page_num, doc)
        self._write_content_to_heading(page_heading, Head("C"), doc)
        page_heading.add_header_item(self._index, self._text)

    def _get_page_header_data(self, data: dict):
        if self._has_reference(data):
            return self._get_reference_data(data)
        return data

    def _get_reference_data(self, data: dict) -> dict:
        ref_index = retrieve_index_from_reference(data)
        return DoclingDataStore().get_text_by_index(ref_index)
