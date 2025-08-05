from .stores.table.table_items_position_store import TableItemsPositionStore
from .stores.paragraph.paragraph_items_position_store import ParagraphItemsPositionStore

class ItemsPositionStoresManager:

    def __init__(self, doc_file_path: str):
        self._paragraph_store = ParagraphItemsPositionStore(doc_file_path)
        self._table_store = TableItemsPositionStore(doc_file_path)

    def get_paragraph_positions_store(self) -> ParagraphItemsPositionStore:
        return self._paragraph_store

    def get_table_positions_store(self) -> TableItemsPositionStore:
        return self._table_store
