from copy import deepcopy

class TableSegmentData:

    def __init__(self):
        self._html = []
        self._otsl = []
        self._has_text_break = False
        self._has_page_break = False

    def has_text_break(self) -> bool:
        return self._has_text_break

    def has_page_break(self) -> bool:
        return self._has_page_break

    def set_text_break(self):
        self._has_text_break = True

    def set_page_break(self):
        self._has_page_break = True

    def add_html(self, html: list[str]):
        self._html += html

    def add_otsl(self, otsl: list[str]):
        self._otsl += otsl

    def to_dict(self) -> dict:
        return {
            "html_seq": deepcopy(self._html),
            "otsl_seq": deepcopy(self._otsl)
        }
