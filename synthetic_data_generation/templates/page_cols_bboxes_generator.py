from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.templates.latex_page_layout_calculator import LatexPageLayoutCalculator
from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.util.unit_converter import UnitConverter

class PageColsBboxesGenerator:

    def __init__(self, layout_style: dict, num_cols: int, col_sep: float):
        self._layout_style = layout_style
        self._num_cols = num_cols
        self._col_sep = col_sep
        self._one_inch_pt = 72
        self._unit_converter = UnitConverter()
        self._page_layout_calculator = LatexPageLayoutCalculator()

    def gen_even_page_cols_bboxes(self) -> list:
        return self._gen_page_cols_bboxes(is_even_page=True)

    def gen_odd_page_cols_bboxes(self) -> list:
        return self._gen_page_cols_bboxes(is_even_page=False)

    def _gen_page_cols_bboxes(self, is_even_page: bool
    ) -> list:
        col_bboxes = []
        col_width = self._calc_page_col_width()
        left = self._calc_page_text_x_origin(is_even_page)
        for _ in range(self._num_cols):
            col_bboxes.append(
                self._gen_page_col_bbox(left, col_width))
            left += col_width + self._col_sep
        return col_bboxes

    def _calc_page_col_width(self) -> float:
        text_width = self._layout_style[TemplateKeys.TEXT_WIDTH]
        cols_width = text_width - ((self._num_cols - 1) * self._col_sep)
        col_width = cols_width / self._num_cols
        return col_width

    def _calc_page_text_x_origin(self, is_even_page: bool) -> float:
        if (is_even_page):
            return self._calc_even_page_text_x_origin()
        return self._calc_odd_page_text_x_origin()

    def _calc_even_page_text_x_origin(self) -> float:
        # Using the geometry package, even and odd pages have the same layout.
        return self._calc_odd_page_text_x_origin()

    def _calc_odd_page_text_x_origin(self) -> float:
        return (self._one_inch_pt + self._layout_style[TemplateKeys.H_OFFSET] +
            self._layout_style[TemplateKeys.ODD_SIDE_MARGIN])

    def _gen_page_col_bbox(self, left, col_width) -> Bbox:
        # Bbox must surround the content. Expand it by 1 px in all directions.
        coordinates = [
            self._unit_converter.pt_to_px(left) - 1,
            self._unit_converter.pt_to_px(
                self._page_layout_calculator.calc_text_y_origin(
                    self._layout_style)) - 1,
            self._unit_converter.pt_to_px(left + col_width) + 1,
            self._unit_converter.pt_to_px(
                self._page_layout_calculator.calc_text_y_end(
                    self._layout_style) + 1)
        ]
        return Bbox(coordinates)
