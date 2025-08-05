from synthetic_data_generation.templates.util.style_item import StyleItem
from .figure_item_style import FigureItemStyle

class OneColFigureItemStyle(FigureItemStyle):

    _line_width_min = 0.4
    _line_width_max = 0.98

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)
