from pylatex import NoEscape, Package

from synthetic_data_generation.templates.template_settings.table_item_settings.wrap_table_item_style import WrapTableItemStyle
from .table_base_env import TableBaseEnv

class WraptableEnv(TableBaseEnv):

    packages = [Package("wrapfig")]
    _latex_name = "wraptable"

    def __init__(self, style: WrapTableItemStyle):
        super().__init__(style, arguments=self._gen_arguments(style))
        self._wrap_position = style.get_float_position()

    def get_wrap_position(self):
        return self._wrap_position

    def _gen_arguments(self, style: WrapTableItemStyle) -> list:
        return [
            style.get_float_position(),
            NoEscape(f"{style.get_line_width()}\linewidth")
        ]
