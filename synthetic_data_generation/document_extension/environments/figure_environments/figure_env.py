from pylatex import NoEscape, Package, UnsafeCommand

from synthetic_data_generation.document_extension.environments.base_env import BaseEnv
from synthetic_data_generation.templates.template_settings.figure_item_settings.figure_item_style import FigureItemStyle

class FigureEnv(BaseEnv):

    packages = [Package("adjustbox", options="export")]
    _latex_name = "figure"

    def __init__(self, style: FigureItemStyle, options=None, arguments=None):
        super().__init__(style, options=options, arguments=arguments)

    def add_image(self, path: str, width=None):
        float_position = self._float_position_to_figure_format()
        if not width:
            #width is a float between 0 and 1.0
            width = self._line_width

        print('line width', self._line_width)
        self.append(
            UnsafeCommand(
                "includegraphics",
                options=[
                    NoEscape(f"width={width}\linewidth"),
                    float_position
                ],
                arguments=NoEscape(path)))

    def _float_position_to_figure_format(self):
        table = {
            "c": "center",
            "l": "left",
            "r": "right"
        }
        try:
            return table[self._float_position]
        except KeyError:
            return ""

    def add_caption(self, text: str):
        self.append(UnsafeCommand("caption", arguments=text))
