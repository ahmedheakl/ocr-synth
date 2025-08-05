import re
from pylatex import MultiColumn, MultiRow, NoEscape

from synthetic_data_generation.serializer.text_serializer.url_to_latex_url_serializer import UrlToLatexUrlSerializer

class TableCellGet:

    def __init__(self, table_cell: dict):
        (left_col_index, top_row_index) = self._extract_top_left(
            table_cell["spans"])
        (right_col_index, bottom_row_index) = self._extract_bottom_right(
            table_cell["spans"])

        self._left_col_index = left_col_index
        self._right_col_index = right_col_index
        self._top_row_index = top_row_index
        self._bottom_row_index = bottom_row_index
        self._bbox = table_cell["bbox"]
        self._text = table_cell["text"]

    def is_two_dim_cell(self) -> bool:
        return (self.is_multirow_cell() and self.is_multicol_cell())

    def is_multirow_cell(self):
        return (self.get_num_rows() > 1)

    def is_multicol_cell(self):
        return (self.get_num_cols() > 1)

    def is_empty(self) -> bool:
        return (self._text == "")


    def get_left_col_index(self):
        return self._left_col_index

    def get_right_col_index(self):
        return self._right_col_index

    def get_top_row_index(self):
        return self._top_row_index

    def get_bottom_row_index(self):
        return self._bottom_row_index

    def get_top_left_coordinate(self):
        return (self._left_col_index, self._top_row_index)

    def get_bottom_right_coordinate(self):
        return (self._right_col_index, self._bottom_row_index)

    def get_coordinates(self):
        return (self._left_col_index, self._top_row_index,
                self._right_col_index, self._bottom_row_index)

    def get_num_cols(self):
        return self._right_col_index - self._left_col_index + 1

    def get_num_rows(self):
        return self._bottom_row_index - self._top_row_index + 1

    def get_bbox(self):
        return self._bbox

    def get_text(self):
        return self._text


    def to_html(self, row_loop_index: int, col_loop_index: int) -> list[str]:
        if (self.is_two_dim_cell()):
            return self._gen_two_dim_cell_html_tags(
                row_loop_index, col_loop_index)
        return self._gen_one_dim_cell_html_tags(row_loop_index, col_loop_index)

    def _gen_one_dim_cell_html_tags(
        self, row_loop_index: int, col_loop_index: int
    ) -> list[str]:
        if (self.is_multirow_cell()):
            if not (self._is_top_cell(row_loop_index)): return []
            start_tag = f"<td {self._gen_rowspan_tag_arg()}>"
        elif (self.is_multicol_cell()):
            if not (self._is_left_cell(col_loop_index)): return []
            start_tag = f"<td {self._gen_colspan_tag_arg()}>"
        else:
            start_tag = "<td>"
        return [start_tag, self._text, "</td>"]

    def _gen_two_dim_cell_html_tags(
        self, row_loop_index: int, col_loop_index: int
    ) -> list[str]:
        if (self._is_top_left_cell(row_loop_index, col_loop_index)):
            rowspan_arg = self._gen_rowspan_tag_arg()
            colspan_arg = self._gen_colspan_tag_arg()
            return [f"<td {rowspan_arg} {colspan_arg}>", self._text, "</td>"]
        return []

    def _gen_rowspan_tag_arg(self) -> str:
        return f"rowspan=\"{self.get_num_rows()}\""

    def _gen_colspan_tag_arg(self) -> str:
        return f"colspan=\"{self.get_num_cols()}\""

    def _is_left_cell(self, col_loop_index: int) -> bool:
        return (self._left_col_index == col_loop_index)

    def _is_top_cell(self, row_loop_index: int) -> bool:
        return (self._top_row_index == row_loop_index)


    def to_otsl(self, row_loop_index: int, col_loop_index: int) -> list[str]:
        if (self.is_two_dim_cell()):
            return self._gen_two_dim_cell_otsl_data(
                row_loop_index, col_loop_index)
        return self._gen_one_dim_cell_otsl_data(row_loop_index, col_loop_index)

    def _gen_one_dim_cell_otsl_data(
        self, row_loop_index: int, col_loop_index: int
    ) -> list[str]:
        if (self.is_multirow_cell()):
            if (self._top_row_index == row_loop_index):
                return self._gen_otsl_data()
            return ["<ucel>"]
        elif (self.is_multicol_cell()):
            if (self._left_col_index == col_loop_index):
                return self._gen_otsl_data()
            return ["<lcel>"]
        return self._gen_otsl_data()

    def _gen_two_dim_cell_otsl_data(
        self, row_loop_index: int, col_loop_index: int
    ) -> list[str]:
        if (self._is_top_left_cell(row_loop_index, col_loop_index)):
            return self._gen_otsl_data()
        return ["<xcel>"]

    def _gen_otsl_data(self) -> list[str]:
        if (self.is_empty()):
            return ["<ecel>", self._text]
        return ["<fcel>", self._text]

    def _is_top_left_cell(
        self, row_loop_index: int, col_loop_index: int
    ) -> bool:
        return ((self._top_row_index == row_loop_index) and
            (self._left_col_index == col_loop_index))


    def to_latex(self, col_width_arg: str="*"):
        row_data = self._gen_row_data(col_width_arg)
        return self._gen_col_data(row_data, col_width_arg)

    def _gen_row_data(self, col_width_arg: str):
        if (self.is_multirow_cell()):
            num_rows = self.get_num_rows()
            width = self._compute_col_width(col_width_arg)
            data = self._gen_cell_text_for_rendering()
            return MultiRow(num_rows, width=width, data=data)
        return self._gen_cell_text_for_rendering()

    def _gen_cell_text_for_rendering(self):
        return self._split_long_unbreakable_char_sequences(self._text)

    def _split_long_unbreakable_char_sequences(self, text):
        return re.sub(r"([^ -]{20})", r"\1 ", text)

    def _gen_col_data(self, row_data, col_width_arg: str):
        if (self.is_multicol_cell()):
            num_cols = self.get_num_cols()
            align = self._gen_multicol_align(col_width_arg)
            return MultiColumn(num_cols, align=align, data=row_data)
        return row_data

    def _gen_multicol_align(self, col_width_arg: str) -> str:
        width = self._compute_col_width(col_width_arg)
        unit = self._extract_unit_from_col_width_arg(col_width_arg)
        return NoEscape("U{" + f"{width}{unit}" + "}")

    def _compute_col_width(self, col_width_arg: str):
        num_cols = self.get_num_cols()
        col_width = self._extract_width_from_col_width_arg(col_width_arg)
        return num_cols * col_width

    def _extract_width_from_col_width_arg(self, col_width_arg: str) -> int:
        return int(re.search(r"[0-9]+", col_width_arg).group())

    def _extract_unit_from_col_width_arg(self, col_width_arg: str) -> str:
        return re.search(r"[a-z]+", col_width_arg).group()

    def _extract_top_left(self, cell_spans: list):
        min_top = 1e6
        min_left = 1e6
        for cell_span in cell_spans:
            if (cell_span[0] < min_top):
                min_top = cell_span[0]
            if (cell_span[1] < min_left):
                min_left = cell_span[1]
        return (min_left, min_top)

    def _extract_bottom_right(self, cell_spans: list):
        max_right = 0
        max_bottom = 0
        for cell_span in cell_spans:
            if (cell_span[0] > max_bottom):
                max_bottom = cell_span[0]
            if (cell_span[1] > max_right):
                max_right = cell_span[1]
        return (max_right, max_bottom)