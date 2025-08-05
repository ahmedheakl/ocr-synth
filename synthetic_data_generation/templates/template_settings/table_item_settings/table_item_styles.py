from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner
from synthetic_data_generation.templates.template_settings.layout_settings.layout_settings import LayoutSettings
from .table_item_style import TableItemStyle
from .all_col_table_item_style import AllColTableItemStyle
from .one_col_table_item_style import OneColTableItemStyle
from .wrap_table_item_style import WrapTableItemStyle

class TableItemStyles:

    def __init__(self, template: dict, num_page_cols: int):
        questioner = TemplateQuestioner(template)
        self._styles = self._gen_styles(questioner)
        self._is_multicol_template = (num_page_cols > 1)

    def get_table_item_style(
        self, pos_type: str, num_table_cols: int
    ) -> TableItemStyle:
        if (self._is_multicol_style_required(num_table_cols)):
            return self._styles[TemplateKeys.ALL_COL_TABLE]
        return self._styles[pos_type]

    def _is_multicol_style_required(self, num_table_cols: int) -> bool:
        return ((self._is_multicol_template) and (num_table_cols >
            LayoutSettings.NUM_TABLE_COLS_MAX_MULTICOL_LAYOUT))

    def _gen_styles(self, questioner: TemplateQuestioner) -> dict:
        styles = {}
        styles[TemplateKeys.ONE_COL_TABLE] = OneColTableItemStyle(
            questioner.get_table_style_item(TemplateKeys.ONE_COL_TABLE))
        styles[TemplateKeys.ALL_COL_TABLE] = AllColTableItemStyle(
            questioner.get_table_style_item(TemplateKeys.ALL_COL_TABLE))
        styles[TemplateKeys.WRAP_TABLE] = WrapTableItemStyle(
            questioner.get_table_style_item(TemplateKeys.WRAP_TABLE))
        return styles
