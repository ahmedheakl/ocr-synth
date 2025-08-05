from pylatex.base_classes import Environment

from synthetic_data_generation.templates.template_settings.util.item_style import ItemStyle

class BaseEnv(Environment):

    escape = False
    content_separator = "%\n"
    _line_width = 1.0

    def __init__(self, style: ItemStyle, options=None, arguments=None):
        super().__init__(options=options, arguments=arguments)
        self._line_width = style.get_line_width()
        self._float_position = style.get_float_position()
        self._add_style(style)

    def get_float_position(self) -> str:
        return self._float_position

    def get_line_width(self) -> float:
        return self._line_width

    def set_line_width(self, line_width: float):
        self._line_width = line_width

    def _add_style(self, style: ItemStyle):
        for command in style.to_latex_commands():
            self.append(command)
