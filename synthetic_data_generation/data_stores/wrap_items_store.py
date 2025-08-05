from synthetic_data_generation.data_stores.wrap_item_store_item import WrapItemStoreItem
from util.latex_item_type_names import LatexItemTypeNames

class WrapItemsStore:

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(WrapItemsStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._data = self._gen_empty_store()

    def clear(self):
        self._data = self._gen_empty_store()

    def add_item(self, item: WrapItemStoreItem) -> bool:
        index = item.get_latex_item_index()
        category = item.get_latex_item_category()
        if (category in self._data):
            self._data[category][index] = item
            return True
        return False

    def get_item(
        self, latex_item_category: str, latex_item_index: int
    )-> WrapItemStoreItem:
        if (self.has_item(latex_item_category, latex_item_index)):
            return self._data[latex_item_category][latex_item_index]
        return None

    def get_item_by_index(self, latex_item_index: int) -> WrapItemStoreItem:
        for category, category_items in self._data.items():
            if latex_item_index in category_items:
                return self._data[category][latex_item_index]

    def has_item(
        self, latex_item_category: str, latex_item_index: int
    ) -> bool:
        if (latex_item_category not in self._data):
            return False
        return latex_item_index in self._data[latex_item_category]

    def has_item_of_index(self, latex_item_index: int) -> bool:
        for category_items in self._data.values():
            if (latex_item_index in category_items):
                return True
        return False

    def _gen_empty_store(self):
        return {
            LatexItemTypeNames.CAPTION: {},
            LatexItemTypeNames.FIGURE: {},
            LatexItemTypeNames.TABLE: {}
        }
