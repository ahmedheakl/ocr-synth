from pylatex import Figure

from synthetic_data_generation.document_extension.environments.figure_environments.multicols_all_col_figure_env import MulticolsAllColFigureEnv
from synthetic_data_generation.document_extension.environments.figure_environments.multicols_one_col_figure_env import MulticolsOneColFigureEnv
from synthetic_data_generation.document_extension.environments.figure_environments.wrapfigure_env import WrapfigureEnv
from synthetic_data_generation.templates.multicols_item_settings.item_col_span_settings import ItemColSpanSettings

class FigureItemColSpanSettings(ItemColSpanSettings):

    _singlecol_envs = {
        ItemColSpanSettings._spans_one_col_key: Figure,
        ItemColSpanSettings._spans_all_col_key: Figure,
        ItemColSpanSettings._wrap_item_key: WrapfigureEnv
    }

    _multicol_envs = {
        ItemColSpanSettings._spans_one_col_key: MulticolsOneColFigureEnv,
        ItemColSpanSettings._spans_all_col_key: MulticolsAllColFigureEnv,
        ItemColSpanSettings._wrap_item_key: WrapfigureEnv
    }

    def __init__(self, template_config: dict):
        display_options_key = "figure"
        super().__init__(template_config, display_options_key)

    def select_env(self):
        return self._select_env(self._get_envs_for_num_cols())

    def _get_envs_for_num_cols(self):
        if (self._num_cols == 1):
            return FigureItemColSpanSettings._singlecol_envs
        return FigureItemColSpanSettings._multicol_envs
