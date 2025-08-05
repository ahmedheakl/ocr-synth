import random

from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class ItemEnvSelector:
    """
    Abstract base class for item env. selection.
    """

    def __init__(self, num_content_cols: int):
        self._num_content_cols = num_content_cols
        self._is_multicol_template = (num_content_cols > 1)

    def select_env(self, pos_type: str):
        if (pos_type == TemplateKeys.RANDOM):
            return self._select_item_env_randomly(pos_type)
        return self._select_active_item_env(pos_type)

    def _select_item_env_randomly(self, pos_type: str):
        if (self._is_multicol_template):
            envs = self._multicol_envs[pos_type]
        else:
            envs = self._singlecol_envs[pos_type]
        return random.choice(list(envs.values()))

    def _select_active_item_env(self, pos_type: str):
        if (self._is_multicol_template):
            return self._multicol_envs[pos_type]
        return self._singlecol_envs[pos_type]
