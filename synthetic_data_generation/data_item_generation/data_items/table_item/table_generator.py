from pylatex import Tabu, LongTabu, NoEscape

from synthetic_data_generation.document_extension.environments.table_environments.multicols_all_col_table_env import MulticolsAllColTableEnv
from synthetic_data_generation.document_extension.type_extension.types.flexible_col_width_left_align_type import FlexibleColWidthLeftAlignType
from synthetic_data_generation.document_extension.type_extension.types.fixed_col_width_left_align_type import FixedColWidthLeftAlignType
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.templates.template_settings.layout_settings.layout_settings import LayoutSettings
import time

class TableGenerator:

    _table_line_width_std_pt = 0.4
    _table_cell_padding_h_std_pt = 6

    def __init__(self, table_item, table_env):
        self._table_item = table_item
        self._line_width = table_env.get_line_width()
        self._table_env_type = type(table_env)
        self._layout_settings = Template().get_layout_settings()

    def table_item_to_latex_table(self):
        table = self._create_table()
        # self._fill_table(table)
        return table

    def _create_table(self):
        if ((self._layout_settings.has_one_col()) or
            (self._table_env_type == MulticolsAllColTableEnv)):
            return Tabu(**self._gen_table_kwargs())
        return Tabu(**self._gen_table_kwargs())

    def _gen_table_kwargs(self) -> dict:
        return {
            "table_spec": self._gen_table_specs(),
            "booktabs": True,
            "pos": ["h", "t"]
        }

    def _gen_table_specs(self) -> str:
        col_separator = ""
        larg = self._gen_length_arg()
        flexible_col_spec = FlexibleColWidthLeftAlignType._latex_name + larg
        fixed_col_spec = FixedColWidthLeftAlignType._latex_name + larg
        table_specs = col_separator
        for _ in range(self._table_item.get_num_cols() - 1):
            table_specs += flexible_col_spec + col_separator
        return table_specs + fixed_col_spec + col_separator

    def _fill_table(self, table):
        length_arg = self._gen_length_arg()
        for row_index, row in enumerate(self._table_item._table_rows):
            table.add_row(row.to_latex(length_arg), strict=False)
            if (row_index + 1 == self._table_item.get_num_rows()): break
            row.add_hline_below(table)

    def _gen_length_arg(self) -> str:
        return "{" + f"{self._compute_col_width_max_pt()}pt" + "}"

    def _compute_col_width_max_pt(self) -> float:
        if (self.requires_multicols_all_col_table_env()):
            col_width = self._layout_settings.get_text_width_pt() * self._line_width * 1.2
        else:
            col_width = self._layout_settings.get_col_width_pt() * self._line_width * 1.2
        table_excess_width = self._compute_table_excess_width_pt()
        return (col_width - table_excess_width) / self._table_item._num_cols

    def requires_multicols_all_col_table_env(self) -> bool:
        if (self._layout_settings.has_one_col()):
            return False
        return (self._table_env_type == MulticolsAllColTableEnv)

    def _compute_table_excess_width_pt(self) -> float:
        padding = (2 * TableGenerator._table_cell_padding_h_std_pt *
            self._table_item.get_num_cols())
        vlines = (TableGenerator._table_line_width_std_pt *
            (self._table_item.get_num_cols() + 1))
        return padding + vlines
