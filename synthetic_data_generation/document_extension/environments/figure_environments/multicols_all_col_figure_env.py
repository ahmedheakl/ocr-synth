from pylatex.package import Package

from .figure_env import FigureEnv
from synthetic_data_generation.templates.template_settings.figure_item_settings.figure_item_style import FigureItemStyle

class MulticolsAllColFigureEnv(FigureEnv):

    packages = [Package("graphicx")]
    _latex_name = "figure*"

    def __init__(self, style: FigureItemStyle):
        super().__init__(style)
