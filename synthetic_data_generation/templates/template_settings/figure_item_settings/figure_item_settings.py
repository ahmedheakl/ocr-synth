from synthetic_data_generation.document_extension.environments.figure_environments.figure_env import FigureEnv
from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner
from .figure_env_selector import FigureEnvSelector
from .figure_item_styles import FigureItemStyles

class FigureItemSettings:

    def __init__(self, template: dict, num_content_cols: int):
        self._figure_env_selector = FigureEnvSelector(num_content_cols)
        self._position_item = (TemplateQuestioner(template).
            get_figure_position_item())
        self._figure_item_styles = FigureItemStyles(template)

    def get_figure_env(self) -> FigureEnv:
        pos_type = self._position_item.get_pos_type()
        env = self._figure_env_selector.select_env(pos_type)
        item_style = self._figure_item_styles.get_figure_item_style(pos_type)
        return env(style=item_style)
