import random
from pylatex import Package, UnsafeCommand

from synthetic_data_generation.templates.available_options.available_font_sizes import AvailableFontSizes
from synthetic_data_generation.templates.util.font_style import FontStyle
from synthetic_data_generation.templates.util.style_item import StyleItem
from synthetic_data_generation.templates.util.template_values import TemplateValues

class ItemStyle:
    """
    Abstract base class for individual item styles.
    """

    _line_width_min = 0.98 # 1.0 can cause issues in multicol formats.
    _line_width_max = 0.98 # 1.0 can cause issues in multicol formats.
    _font_size_min = AvailableFontSizes.NORMALSIZE_INT
    _font_size_max = AvailableFontSizes.NORMALSIZE_INT
    _float_positions = ["c", "l", "r"]
    _default_float_position = ""

    def __init__(self, style_item: StyleItem):
        self._font_color = style_item.get_font_color()
        self._font_size = self._resolve_font_size(style_item.get_font_size())
        self._font_style = style_item.get_font_style()
        self._line_width = self._resolve_line_width(style_item.get_size())
        self._float_position = self._resolve_float_position(
            style_item.get_position())

    def get_font_color(self) -> str:
        return self._font_color

    def get_font_size(self) -> str:
        return self._font_size

    def get_font_style(self) -> FontStyle:
        return self._font_style

    def get_line_width(self) -> float:
        if (TemplateValues.is_random_identifier_float(self._line_width)):
            return random.uniform(self._line_width_min, self._line_width_max)
        return self._line_width

    def get_float_position(self, uppercase: bool=False) -> str:
        if (TemplateValues.is_random_identifier_str(self._float_position)):
            float_position = random.choice(self._float_positions)
        else:
            float_position = self._float_position
        return float_position.upper() if (uppercase) else float_position

    def to_latex_commands(self) -> list[UnsafeCommand]:
        cmds = []
        if (self._font_color is not None):
            cmds.append(UnsafeCommand("color", arguments=self._font_color))
        if (self._font_size is not None):
            cmds.append(UnsafeCommand(self.get_font_size()))
        if (self._font_style is not None):
            font_style = self.get_font_style()
            cmds.append(UnsafeCommand(
                "fontfamily",
                arguments=font_style.get_latex_code(),
                packages=[Package(font_style.get_latex_package_name())]))
            cmds.append(UnsafeCommand("selectfont"))
        return cmds

    def _resolve_font_size(self, font_size: int) -> str:
        if (font_size is None):
            return None
        if ((font_size >= self._font_size_min) and
            (font_size <= self._font_size_max)):
            return AvailableFontSizes.int_size_to_latex_str(font_size)
        return AvailableFontSizes.int_size_to_latex_str(self._font_size_max) 

    def _resolve_line_width(self, size: int) -> float:
        if (TemplateValues.is_random_identifier_int(size)):
            return 0.0 # Random size pick identifier
        range = self._line_width_max - self._line_width_min
        num_steps = size - 1
        step_size = range / (TemplateValues.SIZE_MAX - 1)
        varying_line_width = num_steps * step_size
        return self._line_width_min + varying_line_width

    def _resolve_float_position(self, position: str) -> str:
        if ((TemplateValues.is_random_identifier_str(position)) or
            (position in self._float_positions)):
            return position
        return self._default_float_position
