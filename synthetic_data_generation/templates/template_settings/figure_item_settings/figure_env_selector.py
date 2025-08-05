from synthetic_data_generation.document_extension.environments.figure_environments.figure_env import FigureEnv
from synthetic_data_generation.document_extension.environments.figure_environments.multicols_all_col_figure_env import MulticolsAllColFigureEnv
from synthetic_data_generation.document_extension.environments.figure_environments.multicols_one_col_figure_env import MulticolsOneColFigureEnv
from synthetic_data_generation.document_extension.environments.figure_environments.singlecol_figure_env import SingleColFigureEnv
from synthetic_data_generation.document_extension.environments.figure_environments.wrapfigure_env import WrapfigureEnv
from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.template_settings.util.item_env_selector import ItemEnvSelector

class FigureEnvSelector(ItemEnvSelector):

    _singlecol_envs = {
        TemplateKeys.ONE_COL_FIGURE: SingleColFigureEnv,
        TemplateKeys.ALL_COL_FIGURE: SingleColFigureEnv,
        TemplateKeys.WRAP_FIGURE: WrapfigureEnv
    }

    _multicol_envs = {
        TemplateKeys.ONE_COL_FIGURE: MulticolsOneColFigureEnv,
        TemplateKeys.ALL_COL_FIGURE: MulticolsAllColFigureEnv,
        # Deny wrap functionality for multicol page environments.
        TemplateKeys.WRAP_FIGURE: MulticolsOneColFigureEnv
    }

    def __init__(self, num_content_cols: int):
        super().__init__(num_content_cols)

    def select_env(self, pos_type: str):
        return super().select_env(pos_type)
