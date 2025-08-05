from util.latex_item_type_names import LatexItemTypeNames

from .data_items.text_item.caption_item import CaptionItem
from .data_items.figure_item.figure_item import FigureItem
from .data_items.text_item.footer_item import FooterItem
from .data_items.text_item.header_item import HeaderItem
from .data_items.main_text_item import MainTextItem
from .data_items.text_item .paragraph_item import ParagraphItem
from .data_items.text_item.section_item import SectionItem
from .data_items.table_item.table_item import TableItem
from .data_items.text_item.title_item import TitleItem
from .data_items.text_item.formula_item import FormulaItem
from .data_items.groups_item.inline_item import InlineItem
from .data_items.text_item.code_item import CodeItem

_map = {
    LatexItemTypeNames.CAPTION: CaptionItem,
    LatexItemTypeNames.FIGURE: FigureItem,
    LatexItemTypeNames.FOOTNOTE: FooterItem,
    LatexItemTypeNames.PAGE_FOOTER: FooterItem,
    LatexItemTypeNames.PAGE_HEADER: HeaderItem,
    LatexItemTypeNames.SECTION: SectionItem,
    LatexItemTypeNames.SUBSECTION: SectionItem,
    LatexItemTypeNames.SUBSUBSECTION: SectionItem,
    LatexItemTypeNames.TABLE: TableItem,
    LatexItemTypeNames.TITLE: TitleItem,
    LatexItemTypeNames.FORMULA: FormulaItem,
    LatexItemTypeNames.CODE: CodeItem,
    LatexItemTypeNames.LIST_ITEM: ParagraphItem,
    LatexItemTypeNames.INLINE: InlineItem,
    LatexItemTypeNames.PARAGRAPH: ParagraphItem,
    LatexItemTypeNames.TEXT: ParagraphItem,
    "section": SectionItem,
    "paragraph": ParagraphItem,

}

def data_to_instance(index: int, data: dict) -> MainTextItem:
    item_type = _map[data["label"]]
    return item_type(index, data)
