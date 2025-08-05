from synthetic_data_generation.data_structures.latex_document.page_heading import PageHeading
from synthetic_data_generation.data_structures.latex_document.page_heading_item import PageHeadingItem
from synthetic_data_generation.data_structures.latex_document.page_heading_store import PageHeadingStore
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_data import GroundTruthData
from synthetic_data_generation.templates.available_options.available_items import AvailableItems
from synthetic_data_generation.templates.template import Template

class HeadingBboxOptimizer:

    def __init__(self, gt_data: GroundTruthData):
        self._gt_data = gt_data
        self._layout_settings = Template().get_layout_settings()
        self._page_heading_store = PageHeadingStore()

    def optimize_heading_bboxes(self):
        excluded_ro_items = Template().get_excluded_reading_order_items()
        has_ro_headers = not excluded_ro_items.has_item(
            AvailableItems.PAGE_HEADER)
        has_ro_footers = not excluded_ro_items.has_item(
            AvailableItems.PAGE_FOOTER)
        for page_heading in self._page_heading_store.get_page_headings():
            if (has_ro_headers):
                self._optimize_header_bboxes(page_heading)
            if (has_ro_footers):
                self._optimize_footer_bboxes(page_heading)

    def _optimize_header_bboxes(self, page_heading: PageHeading):
        header_items = page_heading.get_header_items()
        self._optimize_heading_items(
            header_items, self._calc_optimized_header_item_bbox)

    def _optimize_footer_bboxes(self, page_heading: PageHeading):
        footer_items = page_heading.get_footer_items()
        self._optimize_heading_items(
            footer_items, self._calc_optimized_footer_item_bbox)

    def _optimize_heading_items(self, heading_items: list, bbox_optimizer):
        self._current_line_index = 0
        for heading_item in heading_items:
            self._optimize_heading_item_bbox(heading_item, bbox_optimizer)
            self._current_line_index += heading_item.get_num_text_lines()

    def _optimize_heading_item_bbox(
        self, heading_item: PageHeadingItem, bbox_optimizer
    ):
        prov_item = self._get_gt_prov_item(heading_item)
        bbox = prov_item.get_bbox()
        obbox = bbox_optimizer(bbox, heading_item)
        prov_item.set_bbox(obbox)

    def _get_gt_prov_item(self, heading_item: PageHeadingItem):
        index = heading_item.get_reading_order_index()
        gt_item = self._gt_data.get_item(index)
        prov_item_index = 0
        return gt_item.get_prov_item(prov_item_index)

    def _calc_optimized_header_item_bbox(
        self, bbox: list, heading_item: PageHeadingItem
    ):
        head_top = self._layout_settings.get_head_top_px()
        line_height = self._layout_settings.get_baseline_skip_px() - 2
        return self._calc_optimized_item_bbox(
            bbox, head_top, line_height, heading_item)

    def _calc_optimized_footer_item_bbox(
        self, bbox: list, heading_item: PageHeadingItem
    ):
        foot_top = self._layout_settings.get_foot_top_px()
        line_height = self._layout_settings.get_baseline_skip_px()
        return self._calc_optimized_item_bbox(
            bbox, foot_top, line_height, heading_item)

    def _calc_optimized_item_bbox(
        self,
        bbox: list,
        heading_top: int,
        line_height: int,
        heading_item: PageHeadingItem
    ):
        oleft = bbox[0]
        oright = self._layout_settings.get_even_page_text_x_end_px()
        otop = heading_top + self._current_line_index * line_height
        obottom = otop + line_height * heading_item.get_num_text_lines()
        return [oleft, otop, oright, obottom]
