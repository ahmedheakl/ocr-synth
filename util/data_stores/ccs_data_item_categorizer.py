from util.latex_item_type_names import LatexItemTypeNames

class CcsDataItemCategorizer:

    def is_caption(self, item):
        return self._get_type(item) == LatexItemTypeNames.CAPTION

    def is_figure(self, item):
        return (self._get_type(item) == "picture" or
                self._get_type(item) == LatexItemTypeNames.FIGURE)

    def is_footnote(self, item):
        return self._get_type(item) == LatexItemTypeNames.FOOTNOTE

    def is_header(self, item):
        return (self._get_type(item) == LatexItemTypeNames.SECTION or
                self._get_type(item) == LatexItemTypeNames.SUBSECTION or
                self._get_type(item) == LatexItemTypeNames.SUBSUBSECTION)

    def is_page_footer(self, item):
        return self._get_type(item) == LatexItemTypeNames.PAGE_FOOTER

    def is_page_header(self, item):
        return self._get_type(item) == LatexItemTypeNames.PAGE_HEADER

    def is_paragraph(self, item):
        return self._get_type(item) == LatexItemTypeNames.PARAGRAPH

    def is_table(self, item):
        return self._get_type(item) == LatexItemTypeNames.TABLE

    def is_title(self, item):
        return self._get_type(item) == LatexItemTypeNames.TITLE

    def _get_type(self, item: dict) -> str:
        if ((type(item) == dict) and ("type" in item)):
            return item["type"]
        return None
