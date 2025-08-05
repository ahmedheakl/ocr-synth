from pylatex import NoEscape, Package, UnsafeCommand

from synthetic_data_generation.templates.template_settings.figure_item_settings.figure_item_style import FigureItemStyle
from .figure_env import FigureEnv

class WrapfigureEnv(FigureEnv):

    packages = [Package("graphicx"), Package("wrapfig")]
    _latex_name = "wrapfigure"

    def __init__(self, style: FigureItemStyle):
        super().__init__(style, arguments=self._gen_arguments(style))

    def _gen_arguments(self, style: FigureItemStyle) -> list:
        return [
            style.get_float_position(uppercase=True),
            NoEscape(f"{style.get_line_width()}\linewidth")
        ]

    def add_image(self, path: str):
        line_width = 1.0 # Span the whole width of the wrap container.
        self.append(
            UnsafeCommand(
                "includegraphics",
                options=[NoEscape(f"width={line_width}\linewidth")],
                arguments=NoEscape(path)))
