
from pylatex import NoEscape

from synthetic_data_generation.document_extension.command_extension.commands.log_table_row_position_command import LogTableRowPositionCommand
from .table_cell import TableCellGet

class TableRow:

    # Index over all table rows of the doc to identify each row in the tex doc.
    LATEX_LABEL_INDEX = 0

    def __init__(
        self, item_index: int, row_index: int, table_cells: list, num_cols: int
    ):
        self._item_index = item_index
        self._table_cells = table_cells
        self._num_cols = num_cols
        self._row_index = row_index

    def get_num_cols(self) -> int:
        return self._num_cols

    def to_html(self) -> list[str]:
        html_row_tags = ["<tr>"]
        for col_index, table_cell in enumerate(self._table_cells):
            html_row_tags += table_cell.to_html(self._row_index, col_index)
        html_row_tags.append("</tr>")
        return html_row_tags

    def to_otsl(self) -> list[str]:
        otsl_row_cells = []
        for col_index, table_cell in enumerate(self._table_cells):
            otsl_row_cells += table_cell.to_otsl(self._row_index, col_index)
        otsl_row_cells.append("<nl>")
        return otsl_row_cells

    def to_latex(self, col_width_max: str="*"):
        latex_row = []
        for col_index, table_cell in enumerate(self._table_cells):
            if (self._is_first_col_of_table_cell(table_cell, col_index)):
                self._add_table_cell_to_latex_row(table_cell, latex_row,
                                                  col_width_max)
        self._add_log_file_cmd(latex_row)
        self._increment_latex_label_index()
        return latex_row

    def _is_first_col_of_table_cell(sefl, table_cell, col_index):
        return (table_cell.start_col_offset_idx == col_index)

    def _add_table_cell_to_latex_row(
            self, table_cell: TableCellGet, latex_row, col_width_max: str):
        if (self._is_first_row_of_table_cell(table_cell)):
            latex_row.append(table_cell.to_latex(col_width_max))
        else:
            self._fill_multidim_cells_with_placeholder(table_cell, latex_row)

    def _is_first_row_of_table_cell(self, table_cell):
        return (table_cell.start_row_offset_idx == self._row_index)

    def _fill_multidim_cells_with_placeholder(self, table_cell, latex_row):
        for _ in range(table_cell.get_num_cols()):
            latex_row.append("")

    def _add_log_file_cmd(self, latex_row: list[str]):
        if (self._is_single_cell(latex_row[0])):
            latex_row[0] = NoEscape(self._gen_row_index_log_cmd() +
                latex_row[0])
        else:
            latex_row[0].data.append(NoEscape(self._gen_row_index_log_cmd()))

    def _is_single_cell(self, first_col_cell) -> bool:
        return (type(first_col_cell) == str)

    def _gen_row_index_log_cmd(self) -> str:
        return (f"\\{LogTableRowPositionCommand().get_latex_name()}"
            "{" + str(self._item_index) + "}"
            "{" + str(self._row_index) + "}"
            "{" + f"trlabel{TableRow.LATEX_LABEL_INDEX}" + "}")

    def _increment_latex_label_index(self):
        TableRow.LATEX_LABEL_INDEX += 1

    def add_hline_below(self, table):
        for table_cell in self._table_cells:
            if (self._is_last_row_of_table_cell(table_cell)):
                table.add_hline(table_cell.start_col_offset_idx() + 1,
                    table_cell.get_right_col_index() + 1)

    def _is_last_row_of_table_cell(self, table_cell):
        return (table_cell.get_bottom_row_index() == self._row_index)