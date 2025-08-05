from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner
from .figure_item_style import FigureItemStyle
from .all_col_figure_item_style import AllColFigureItemStyle
from .one_col_figure_item_style import OneColFigureItemStyle
from .wrap_figure_item_style import WrapFigureItemStyle

class FigureItemStyles:

    def __init__(self, template: dict):
        self._styles = self._gen_styles(template)

    def get_figure_item_style(self, pos_type: str) -> FigureItemStyle:
        return self._styles[pos_type]

    def _gen_styles(self, template: dict) -> dict:
        styles = {}
        questioner = TemplateQuestioner(template)
        styles[TemplateKeys.ONE_COL_FIGURE] = OneColFigureItemStyle(
            questioner.get_figure_style_item(TemplateKeys.ONE_COL_FIGURE))
        styles[TemplateKeys.ALL_COL_FIGURE] = AllColFigureItemStyle(
            questioner.get_figure_style_item(TemplateKeys.ALL_COL_FIGURE))
        styles[TemplateKeys.WRAP_FIGURE] = WrapFigureItemStyle(
            questioner.get_figure_style_item(TemplateKeys.WRAP_FIGURE))
        return styles
