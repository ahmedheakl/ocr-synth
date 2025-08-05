from synthetic_data_generation.document_extension.environments.null_env import NullEnv
from synthetic_data_generation.document_extension.environments.table_environments.multicols_all_col_table_env import MulticolsAllColTableEnv
from synthetic_data_generation.document_extension.environments.table_environments.multicols_one_col_table_env import MulticolsOneColTableEnv
from synthetic_data_generation.document_extension.environments.table_environments.wraptable_env import WraptableEnv
from synthetic_data_generation.templates.multicols_item_settings.item_col_span_settings import ItemColSpanSettings

class TableItemColSpanSettings(ItemColSpanSettings):

    _singlecol_envs = {
        ItemColSpanSettings._spans_one_col_key: NullEnv,
        ItemColSpanSettings._spans_all_col_key: NullEnv,
        ItemColSpanSettings._wrap_item_key: WraptableEnv
    }

    _multicol_envs = {
        ItemColSpanSettings._spans_one_col_key: MulticolsOneColTableEnv,
        ItemColSpanSettings._spans_all_col_key: MulticolsAllColTableEnv,
        # Deny wrap functionality for multicol page environments.
        ItemColSpanSettings._wrap_item_key: MulticolsOneColTableEnv
    }

    def __init__(
        self, template_config: dict, num_table_cols_max_on_multicol_page: int
    ):
        display_options_key = "table"
        super().__init__(template_config, display_options_key)
        self._num_table_cols_max_on_multicol_page = num_table_cols_max_on_multicol_page

    def select_env(self, num_rows: int, num_cols: int):
        if (self._num_cols == 1):
            return self._select_single_col_page_env(num_rows)
        return self._select_multicol_page_env(num_cols)

    def _select_single_col_page_env(self, num_rows: int):
        if (num_rows > 6):
            return NullEnv
        return self._select_env(TableItemColSpanSettings._singlecol_envs)

    def _select_multicol_page_env(self, num_cols: int):
        if (num_cols > self._num_table_cols_max_on_multicol_page):
            return MulticolsAllColTableEnv
        return self._select_env(TableItemColSpanSettings._multicol_envs)
