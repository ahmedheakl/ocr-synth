from copy import deepcopy

from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.templates.template import Template
from util.latex_item_type_names import LatexItemTypeNames

class LineNumBboxGenerator:

    _line_num_bbox_height = 7 # [px]
    _line_num_bbox_width = 5 # [px]
    _bbox_paddig_top = 2 # [px]
    _bbox_width_unoptimized_min = 40 # [px]

    def __init__(self):
        self._layout_settings = Template().get_layout_settings()
        self._line_height = self._layout_settings.get_baseline_skip_px()

    def gen_line_num_bboxes_for_main_text_item(
        self, item_type: str, main_text_item_bboxes: list[Bbox]
    ) -> list[Bbox]:
        line_num_bboxes = []
        if not (self._are_line_nums_bboxes_required()):
            return line_num_bboxes
        for main_text_item_bbox in main_text_item_bboxes:
            line_num_bboxes += self._gen_line_num_bboxes(
                item_type, main_text_item_bbox)
        return line_num_bboxes

    def _are_line_nums_bboxes_required(self) -> bool:
        line_nums_settings = Template().get_line_nums_settings()
        return (line_nums_settings.are_displayed() and
            line_nums_settings.are_in_ro())

    def _gen_line_num_bboxes(
        self, item_type: str, item_bbox: Bbox
    ) -> list[Bbox]:
        if (self._is_paragraph_item(item_type)):
            return self._gen_paragraph_line_nums_bboxes(item_bbox)
        elif (self._is_title_or_section_item(item_type)):
            return self._gen_title_or_section_line_nums_bboxes(item_bbox)
        return []

    def _is_paragraph_item(self, item_type: str) -> bool:
        return (item_type == LatexItemTypeNames.PARAGRAPH)

    def _is_title_or_section_item(self, item_type: str) -> bool:
        item_categories = [
            LatexItemTypeNames.SECTION,
            LatexItemTypeNames.SUBSECTION,
            LatexItemTypeNames.SUBSUBSECTION,
            LatexItemTypeNames.TITLE
        ]
        return (item_type in item_categories)

    def _gen_paragraph_line_nums_bboxes(self, item_bbox: Bbox) -> list[Bbox]:
        line_num_bboxes = []
        num_line_bboxes = self._compute_num_line_bboxes(item_bbox)
        bbox_bottom = self._compute_first_line_num_bbox_bottom(
            item_bbox, num_line_bboxes)
        (left, right) = self._compute_line_num_bbox_hcoordinates(item_bbox)
        for _ in range(num_line_bboxes):
            line_bbox = deepcopy(item_bbox)
            line_bbox.set_left(left)
            line_bbox.set_right(right)
            line_bbox.set_bottom(bbox_bottom)
            line_bbox.set_top(
                bbox_bottom - LineNumBboxGenerator._line_num_bbox_height -
                LineNumBboxGenerator._bbox_paddig_top)
            line_num_bboxes.append(line_bbox)
            bbox_bottom += self._line_height
        return line_num_bboxes

    def _gen_title_or_section_line_nums_bboxes(self, item_bbox: Bbox) -> Bbox:
        """
        Creates several line nums bboxes next to the header in aequidistant
        steps. The step size was determined via trial-and-error. As header
        bboxes appear in many different heights before optimization, there is
        no way to determine the exact position of line nums bboxes.
        """
        line_nums_bbox_height = self._line_height * 0.7 # [px] Hyperparameter
        line_num_bboxes = []
        num_line_bboxes = self._compute_num_line_bboxes(item_bbox)
        bbox_bottom = item_bbox.get_bottom()
        (left, right) = self._compute_line_num_bbox_hcoordinates(item_bbox)
        for _ in range(num_line_bboxes):
            line_bbox = deepcopy(item_bbox)
            line_bbox.set_left(left)
            line_bbox.set_right(right)
            line_bbox.set_bottom(bbox_bottom)
            line_bbox.set_top(bbox_bottom - line_nums_bbox_height)
            line_num_bboxes.append(line_bbox)
            bbox_bottom -= self._line_height * 1
        return line_num_bboxes

    def _compute_num_line_bboxes(self, item_bbox: Bbox) -> int:
        bbox_height = item_bbox.get_height()
        # Add some margin to ensure that the number of line numbers is not
        # too few by one (this happens w/o this margin on some occasions).
        margin = self._layout_settings.get_baseline_skip_px() / 2
        return max(1, int((bbox_height + margin) / self._line_height))

    def _compute_first_line_num_bbox_bottom(
        self, item_bbox: Bbox, num_line_bboxes: int
    ) -> int:
        # Items that are at the bottom of a page have their bbox expanded to
        # the bottom edge of the textarea. However, the text might not
        # exactly fill this space. Thus, counting the line num positions from
        # the top of such bboxes is the better option.
        if (item_bbox.get_bottom() ==
            self._layout_settings.get_text_y_end_px()):
            return item_bbox.get_top() + self._line_height + 1
        return (item_bbox.get_bottom() -
            (num_line_bboxes - 1) * self._line_height) + 1

    def _compute_line_num_bbox_hcoordinates(self, item_bbox: Bbox) -> tuple[int, int]:
        right = self._compute_line_num_bbox_right(item_bbox)
        left = self._compute_line_num_bbox_left(right)
        return (left, right)

    def _compute_line_num_bbox_right(self, item_bbox: Bbox) -> int:
        page_cols_bboxes = self._layout_settings.get_page_cols_bboxes(
            item_bbox.get_page_num())
        index = 0
        for page_cols_bbox in page_cols_bboxes:
            if (page_cols_bbox.get_right() < item_bbox.get_left()):
                index += 1
            else: break
        right = page_cols_bboxes[index].get_left()
        return right

    def _compute_line_num_bbox_left(self, right: int) -> int:
        if (self._layout_settings.get_col_sep_px()):
            bbox_line_width = 1 # [px]
            width = (self._layout_settings.get_col_sep_px() -
                2 * bbox_line_width)
        else:
            width = LineNumBboxGenerator._bbox_width_unoptimized_min
        left = right - width
        return left
