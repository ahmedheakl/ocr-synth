from pylatex import LargeText, MiniPage, NewLine, VerticalSpace
from pylatex.utils import bold

from .text_item import TextItem
from pylatex import FlushRight, MiniPage, NewLine, VerticalSpace
from pylatex.utils import NoEscape

class TitleItem(TextItem):

    def __init__(self, index, data: dict):
        super().__init__(index, data)

    def add_as_latex_to_doc(self, doc):
        return
        # doc.log_write_position(self._index)
        # self._add_title_mini_page(doc)
        # doc.log_write_position(self._index)

    def _add_title_mini_page(self, doc):
        return
        width = r"0.9\linewidth"

        # doc.append(NewLine())
        # with doc.create(FlushRight()) as right:
        #     with right.create(MiniPage(width=NoEscape(width))) as mp:
        #         mp.append(VerticalSpace("12pt"))
        #         mp.append(self._gen_render_text())
        #         mp.append(VerticalSpace("18pt"))
        # doc.append(NewLine())

    def _gen_render_text(self):
        render_text = self._split_long_unbreakable_char_sequences(self._text)
        return LargeText(bold(render_text))
