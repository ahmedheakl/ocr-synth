from synthetic_data_generation.document_extension.environments.base_env import BaseEnv
from synthetic_data_generation.document_extension.environments.table_environments.multicols_all_col_table_env import MulticolsAllColTableEnv
from synthetic_data_generation.document_extension.environments.table_environments.multicols_one_col_table_env import MulticolsOneColTableEnv
from synthetic_data_generation.document_extension.environments.table_environments.wraptable_env import WraptableEnv
from synthetic_data_generation.templates.template_settings.layout_settings.layout_settings import LayoutSettings
from synthetic_data_generation.templates.template_settings.util.item_env_selector import ItemEnvSelector
from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class TableEnvSelector(ItemEnvSelector):

    _singlecol_envs = {
        TemplateKeys.ONE_COL_TABLE: BaseEnv,
        TemplateKeys.ALL_COL_TABLE: BaseEnv,
        TemplateKeys.WRAP_TABLE: WraptableEnv
    }

    _multicol_envs = {
        TemplateKeys.ONE_COL_TABLE: MulticolsAllColTableEnv,
        TemplateKeys.ALL_COL_TABLE: MulticolsAllColTableEnv,
        # MulticolsOneColTableEnv
        # Deny wrap functionality for multicol page environments.
        TemplateKeys.WRAP_TABLE: MulticolsAllColTableEnv
        # MulticolsAllColTableEnv was creating some problem in the recognition of
        # a table, therefore I removed it, you can try to fix it if you are reading
    }

    def __init__(self, num_content_cols: int):
        super().__init__(num_content_cols)

    def select_env(
        self, pos_type: str, num_table_rows: int, num_table_cols: int
    ):
        if (self._is_all_col_multicol_env_required(
            num_table_rows, num_table_cols)):
            return TableEnvSelector._multicol_envs[TemplateKeys.ALL_COL_TABLE]
        return super().select_env(pos_type)

    def _is_all_col_multicol_env_required(
        self, num_table_rows: int, num_table_cols: int
    ) -> bool:
        if not (self._is_multicol_template):
            return False
        if (self._num_content_cols > 2):
            return True
        return (
            (num_table_rows >
             LayoutSettings.NUM_TABLE_ROWS_MAX_MULTICOL_LAYOUT) or
            (num_table_cols >
             LayoutSettings.NUM_TABLE_COLS_MAX_MULTICOL_LAYOUT))
