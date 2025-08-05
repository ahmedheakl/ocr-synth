from synthetic_data_generation.data_stores.target_latex_document_store import TargetLatexDocumentStore
from synthetic_data_generation.serializer.write_position_serializer.bbox_optimizer.bbox_optimizer import BboxOptimizer
from synthetic_data_generation.templates.template import Template

class PageBboxBoundsScanner:

    def __init__(self):
        self._layout_settings = Template().get_layout_settings()

    def scan_page_for_vertical_bbox_bounds(
        self, page_num: int
    ) -> tuple[int, int]:
        if (self._layout_settings.has_one_col()):
            return self._get_vertical_textarea_bounds()
        return self._compute_multicol_vertical_bbox_bounds(page_num)
    
    def _compute_multicol_vertical_bbox_bounds(
        self, page_num: int
    ) -> tuple[int, int]:
        page_index = page_num - 1
        page_image = TargetLatexDocumentStore().get_page_image(page_index)
        col_sep_bbox = self._gen_col_sep_bbox(page_num)
        if (self._is_multicol_item_on_page(col_sep_bbox, page_image)):
            return self._compute_vertical_bbox_bounds(
                col_sep_bbox, page_image)
        return self._get_vertical_textarea_bounds()

    def _gen_col_sep_bbox(self, page_num):
        bbox_left = self._compute_col_sep_bbox_left(page_num)
        bbox_right = bbox_left + self._layout_settings.get_col_sep_px()
        bbox_top = self._layout_settings.get_text_y_origin_px()
        bbox_bottom = self._layout_settings.get_text_y_end_px()
        bbox = [bbox_left, bbox_top, bbox_right, bbox_bottom]
        self._narrow_col_sep_bbox_width(bbox)
        return bbox

    def _compute_col_sep_bbox_left(self, page_num: int):
        text_left = self._layout_settings.get_page_text_x_origin_px(page_num)
        col_width = self._layout_settings.get_col_width_px()
        col_sep = self._layout_settings.get_col_sep_px()
        num_cols_left_to_sep = self._layout_settings.get_num_cols() // 2
        num_col_seps_left_to_sep = num_cols_left_to_sep - 1
        col_width_left_to_sep = num_cols_left_to_sep * col_width
        col_sep_width_left_to_sep = num_col_seps_left_to_sep * col_sep
        return text_left + col_width_left_to_sep + col_sep_width_left_to_sep

    def _narrow_col_sep_bbox_width(self, col_sep_bbox: list):
        self._subtract_res_distortion_margin_from_width(col_sep_bbox)
        self._narrow_to_max_width(col_sep_bbox)

    def _subtract_res_distortion_margin_from_width(self, col_sep_bbox: list):
        """
        The loading of the page images distorts the page image resolution. Some
        pixel artefacts might spill over into the otherwise clean column
        separation region. By narrowing the bbox width, only a clean (white)
        region remains if no multicol item is on the page.
        """
        safety_margin = 2 # [px]
        col_sep_bbox[0] += safety_margin
        col_sep_bbox[2] -= safety_margin

    def _narrow_to_max_width(self, col_sep_bbox: list):
        """
        In multicol latex templates, long words might not be broken up at the
        right place and spill over into the page content column separation.
        Thus, a false top coordinate is found for the content column top.
        To avoid this issue, 'left' of the separation bbox is shifted to the
        right as much as possible.
        """
        max_width = 8 # [px] Value estimated by trial and error.
        width = col_sep_bbox[2] - col_sep_bbox[0]
        if (width > max_width):
            delta = width - max_width
            col_sep_bbox[0] += delta

    def _is_multicol_item_on_page(self, col_sep_bbox: list, page_image):
        return BboxOptimizer().bbox_has_content(col_sep_bbox, page_image)

    def _compute_vertical_bbox_bounds(
        self, col_sep_bbox: list, page_image
    ) -> tuple[int, int]:
        optimized_bottom = BboxOptimizer().optimize_bottom(
            col_sep_bbox, page_image)
        # Add margin to ensure col bboxes do not contain multicol item content.
        safety_margin = 4
        margin = self._layout_settings.get_baseline_skip_px() + safety_margin
        page_col_top = optimized_bottom + margin
        page_col_bottom = self._layout_settings.get_text_y_end_px()
        return (page_col_top, page_col_bottom)

    def _get_vertical_textarea_bounds(self) -> tuple[int, int]:
        return (
            self._layout_settings.get_text_y_origin_px(),
            self._layout_settings.get_text_y_end_px()
        )
