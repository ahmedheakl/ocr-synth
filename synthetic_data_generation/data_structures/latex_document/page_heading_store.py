from pylatex import PageStyle

from .page_heading import PageHeading

class PageHeadingStore:

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(PageHeadingStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._page_headings = {}
        self._page_headings_name = "heading"
        self._page_headings_cnt = 0

    def clear(self):
        self._page_headings = {}
        self._page_headings_cnt = 0

    def get_page_heading(self, page_num: int, doc):
        return self._get_or_create_page_heading(page_num, doc)

    def get_page_headings(self):
        return self._page_headings.values()

    def _get_or_create_page_heading(self, page_num: int, doc):
        if not (self._has_page_heading(page_num)):
            self._create_page_heading(page_num, doc)
        return self._page_headings[page_num]

    def _has_page_heading(self, page_num: int):
        return (page_num in self._page_headings)

    def _create_page_heading(self, page_num: int, doc):
        name = f"{self._page_headings_name}{self._page_headings_cnt}"
        self._page_headings_cnt += 1
        page_style = PageStyle(name)
        doc.preamble.append(page_style)
        doc.change_page_style(name)
        self._page_headings[page_num] = PageHeading(page_style)
