from synthetic_data_generation.templates.available_options.available_font_sizes import AvailableFontSizes
from synthetic_data_generation.templates.util.style_item import StyleItem
from .figure_item_style import FigureItemStyle

class WrapFigureItemStyle(FigureItemStyle):

    _font_size_max = AvailableFontSizes.FOOTNOTESIZE_INT
    # Line widths above 0.32 caused issues with caption bbox ground truths.
    # The bboxes do not remain within the wrap region for small figures.
    _line_width_min = 0.15
    _line_width_max = 0.32
    _float_positions = ["l", "r"]
    _default_float_position = "r"

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)
