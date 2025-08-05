from pylatex import Package, UnsafeCommand

from synthetic_data_generation.templates.available_options.available_font_sizes import AvailableFontSizes
from synthetic_data_generation.templates.template_settings.util.item_style import ItemStyle
from synthetic_data_generation.templates.util.style_item import StyleItem

class FigureItemStyle(ItemStyle):

    _font_size_min = AvailableFontSizes.SCRIPTSIZE_INT
    _font_size_max = AvailableFontSizes.NORMALSIZE_INT
    _float_positions = ["c", "l", "r"]
    _default_float_position = "c"

    def __init__(self, style_item: StyleItem):
        super().__init__(style_item)

    def to_latex_commands(self) -> list[UnsafeCommand]:
        format_name = "customcaptionformat" # Defined in custom_document.py
        format = f"format={format_name}"
        size = f"{self.get_font_size()}"
        color = f"color={self.get_font_color()}"
        arguments = format + "," + "font={" + size + "," + color + "}"
        cmd = UnsafeCommand("captionsetup", arguments=arguments,
            packages=[Package("caption")])
        return [cmd]
