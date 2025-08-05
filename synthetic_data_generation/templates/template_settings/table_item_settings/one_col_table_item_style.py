from synthetic_data_generation.templates.util.style_item import StyleItem
from .table_item_style import TableItemStyle

class OneColTableItemStyle(TableItemStyle):

    _line_width_min = 0.98
    _line_width_max = 0.98

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)
