from pylatex import Package

from synthetic_data_generation.templates.template_settings.figure_item_settings.figure_item_style import FigureItemStyle
from .figure_env import FigureEnv

class SingleColFigureEnv(FigureEnv):

    packages = [Package("graphicx"), Package("float")]
    _latex_name = "figure"

    def __init__(self, style: FigureItemStyle):
        options=["H"] # Without a set float option, figures are not shown.
        super().__init__(style, options=options)
