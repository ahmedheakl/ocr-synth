import random

class ItemColSpanSettings:

    _spans_one_col_key = "spans-one-column"
    _spans_all_col_key = "spans-all-column"
    _wrap_item_key = "wrap"
    _random_key = "random"

    _config_figure_key = "figure"
    _config_table_key = "table"

    def __init__(self, template_config: dict, display_options_key: str):
        self._num_cols = template_config["num-columns"]
        self._display_options = self._gen_display_options()
        self._configure_col_template_display_options(
            template_config, display_options_key)

    def _gen_display_options(self):
        return {
            ItemColSpanSettings._spans_all_col_key: False,
            ItemColSpanSettings._spans_one_col_key: False,
            ItemColSpanSettings._wrap_item_key: False,
            ItemColSpanSettings._random_key: False
        }

    def _configure_one_col_template_display_options(self):
        self._display_options[ItemColSpanSettings._one_col_template_key] = True

    def _configure_col_template_display_options(
        self, config: dict, display_options_key: str
    ):
        self._update_display_options(config, display_options_key)
        if (self._has_multiple_active_options()):
            self._set_random_env_selection()

    def _update_display_options(self, config: dict, display_options_key: str):
        config_display_options = config[display_options_key]
        for key in self._display_options:
            if key in config_display_options:
                self._display_options[key] = config_display_options[key]

    def _has_multiple_active_options(self):
        cnt_true = 0
        for value in self._display_options.values():
            if (value):
                cnt_true += 1
        if (cnt_true != 1):
            self._display_options[ItemColSpanSettings._random_key] = True

    def _set_random_env_selection(self):
        self._display_options[ItemColSpanSettings._random_key] = True

    def _select_env(self, envs: dict):
        if self._is_random_selection_configured():
            return self._select_env_randomly(envs)
        return self._select_env_according_to_template_config(envs)

    def _select_env_randomly(self, envs: dict):
        return random.choice(list(envs.values()))

    def _select_env_according_to_template_config(self, envs: dict):
        for key, value in self._display_options.items():
            if (value): return envs[key]

    def _is_random_selection_configured(self):
        return self._display_options[ItemColSpanSettings._random_key]
