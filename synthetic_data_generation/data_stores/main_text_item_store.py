from synthetic_data_generation.data_item_generation.data_items.main_text_item import MainTextItem

class MainTextItemStore:

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(MainTextItemStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._data = {}

    def get_item(self, index: int) -> MainTextItem:
        if (index in self._data):
            return self._data[index]
        return None

    def add_item(self, item: MainTextItem):
        self._data[item.get_index()] = item

    def clear(self):
        self._data = {}
