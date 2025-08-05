from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner
from .table_env_selector import TableEnvSelector
from .table_item_styles import TableItemStyles

class TableItemSettings:

    def __init__(self, template: dict, num_content_cols: int):
        self._table_env_selector = TableEnvSelector(num_content_cols)
        self._position_item = (TemplateQuestioner(template).
            get_table_position_item())
        self._table_item_styles = TableItemStyles(template, num_content_cols)

    def get_table_env(self, num_table_rows: int, num_table_cols: int):
        pos_type = self._position_item.get_pos_type()
        env = self._table_env_selector.select_env(
            pos_type, num_table_rows, num_table_cols)
        item_style = self._table_item_styles.get_table_item_style(
            pos_type, num_table_cols)
        return env(style=item_style)
