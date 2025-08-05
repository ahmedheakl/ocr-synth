import random

from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.util.template_values import TemplateValues

class ContentColsConfigurer:
    """
    Computes all content column settings that form part of the layout settings.
    """

    def __init__(self, layout_style: dict):
        self._num_content_cols = self._configure_num_content_cols(layout_style)
        self._col_sep = self._configure_col_sep(self._num_content_cols)
        self._col_width = self._configure_col_width(
            layout_style[TemplateKeys.TEXT_WIDTH], self._num_content_cols,
            self._col_sep)

    def configure_num_content_cols(self) -> int:
        return self._num_content_cols

    def configure_col_sep(self) -> float:
        return self._col_sep

    def configure_col_width(self) -> float:
        return self._col_width

    def _configure_num_content_cols(self, layout_style: dict) -> int:
        if (TemplateKeys.NUM_CONTENT_COLS not in layout_style):
            return 1
        num_content_cols = layout_style[TemplateKeys.NUM_CONTENT_COLS]
        if (type(num_content_cols) != int):
            return 1
        if (layout_style[TemplateKeys.PAGE_FORMAT] == TemplateValues.PORTRAIT):
            return self._select_portrait_num_content_cols(num_content_cols)
        return self._select_landscape_num_content_cols(num_content_cols)

    def _select_portrait_num_content_cols(self, num_content_cols: int) -> int:
        num_content_cols_choices = [1, 2, 3]
        return self._select_num_content_cols_from_choices(
            num_content_cols, num_content_cols_choices)

    def _select_landscape_num_content_cols(self, num_content_cols: int) -> int:
        num_content_cols_choices = [1, 2, 3, 4]
        return self._select_num_content_cols_from_choices(
            num_content_cols, num_content_cols_choices)

    def _select_num_content_cols_from_choices(
        self, num_content_cols: int, content_cols_choices: list[int]
    ) -> int:
        if (TemplateValues.is_random_identifier_int(num_content_cols)):
            return random.choice(content_cols_choices)
        if (num_content_cols in content_cols_choices):
            return num_content_cols
        return 1

    def _configure_col_sep(self, num_content_cols: int) -> float:
        map = {
            1: 0,
            2: 28.3465,
            3: 22.6772,
            4: 14.1732 # Only used for landscape mode
        }
        return map[num_content_cols]

    def _configure_col_width(
        self, text_width: float, num_cols: int, col_sep: float
    ) -> float:
        total_col_sep_width = (num_cols - 1) * col_sep
        return (text_width - total_col_sep_width) / num_cols
