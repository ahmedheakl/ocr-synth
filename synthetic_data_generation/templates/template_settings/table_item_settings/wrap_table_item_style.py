from synthetic_data_generation.templates.util.style_item import StyleItem
from .table_item_style import TableItemStyle

class WrapTableItemStyle(TableItemStyle):

    _line_width_min = 0.5
    _line_width_max = 0.8
    _default_float_position = "r"

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)
