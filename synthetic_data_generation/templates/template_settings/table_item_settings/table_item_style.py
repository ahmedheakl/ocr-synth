import random

from synthetic_data_generation.templates.available_options.available_font_sizes import AvailableFontSizes
from synthetic_data_generation.templates.template_settings.util.item_style import ItemStyle
from synthetic_data_generation.templates.util.style_item import StyleItem
from synthetic_data_generation.templates.util.template_values import TemplateValues

class TableItemStyle(ItemStyle):
    """
    Abstract parent class for individual table item styles classes.
    """

    _font_size_min = AvailableFontSizes.SCRIPTSIZE_INT
    _font_size_max = AvailableFontSizes.SMALL_INT
    _cell_positions = ["c", "l", "r"]
    _default_float_position = "c"

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)
        self._cell_position = style_item.get_cell_position()

    def get_cell_position(self) -> str:
        if (TemplateValues.is_random_identifier_str(self._cell_position)):
            return random.choice(TableItemStyle._cell_positions)
        return self._cell_position
