from synthetic_data_generation.templates.util.style_item import StyleItem
from .figure_item_style import FigureItemStyle

class AllColFigureItemStyle(FigureItemStyle):

    _line_width_min = 0.3
    _line_width_max = 0.7
    # Figures spanning over all columns are always centered. The bbox GT
    # algorithm depends on this setting. It is necessary to compute the bbox
    # top coordinate correctly.
    _float_positions = ["c"]

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)
