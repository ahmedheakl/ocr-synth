from .page_heading_item import PageHeadingItem

class PageHeading:

    def __init__(self, page_style):
        self._page_style = page_style
        self._header_items = {}
        self._footer_items = {}

    def get_page_style(self):
        return self._page_style

    def get_header_items(self):
        return self._header_items.values()

    def get_footer_items(self):
        return self._footer_items.values()

    def add_header_item(self, index, text):
        item = PageHeadingItem(index, text)
        self._header_items[index] = item

    def add_footer_item(self, index, text):
        item = PageHeadingItem(index, text)
        self._footer_items[index] = item
