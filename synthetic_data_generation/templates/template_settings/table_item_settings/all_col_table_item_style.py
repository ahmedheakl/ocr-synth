from synthetic_data_generation.templates.util.style_item import StyleItem
from .table_item_style import TableItemStyle

class AllColTableItemStyle(TableItemStyle):

    _line_width_min = 1.0
    _line_width_max = 1.0

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)
