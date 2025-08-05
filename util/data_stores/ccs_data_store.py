from util import ccs_data_manager

class CcsDataStore:

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(CcsDataStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._data = None

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def get_ref_item_by_main_text_item_index(self, index):
        main_text_item = self.get_main_text_item(index)
        if (main_text_item is None): return None
        category = main_text_item["type"] + "s"
        ref_index = ccs_data_manager.get_item_ref_index(main_text_item)
        return self.get_data_item(category, ref_index)

    def get_data_item(self, category: str, index):
        return self._data[category][index]

    def get_main_text(self):
        return self._data["main-text"]

    def get_main_text_item(self, index):
        return self._get_item("main-text", index)

    def get_figures(self):
        return self._data["figures"]

    def get_figure_item(self, index):
        return self._get_item("figures", index)

    def get_tables(self):
        return self._data["tables"]

    def get_table_item(self, index):
        return self._get_item("tables", index)

    def get_page_headers(self):
        return self._data["page-headers"]

    def get_page_header_item(self, index):
        return self._get_item("page-headers", index)

    def get_page_footers(self):
        return self._data["page-footers"]

    def get_page_footer_item(self, index):
        return self._get_item("page-footers", index)

    def get_page_dimensions(self):
        return self._data["page-dimensions"]

    def clear(self):
        self._data = None

    def _get_item(self, type: str, index: int):
        try:
            return self._data[type][index]
        except:
            return None
