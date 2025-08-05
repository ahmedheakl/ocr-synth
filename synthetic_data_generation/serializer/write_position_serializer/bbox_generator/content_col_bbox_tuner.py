from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_position import ContentPosition
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData
from synthetic_data_generation.templates.template import Template
from util.data_stores.ccs_data_store import CcsDataStore
from util.data_stores.ccs_data_item_categorizer import CcsDataItemCategorizer

class ContentColBboxTuner:

    def __init__(self):
        self._ccs_data_store = CcsDataStore()
        self._ccs_data_item_categorizer = CcsDataItemCategorizer()
        self._layout_settings = Template().get_layout_settings()

    def tune_first_content_col_bbox(
        self,
        content_col_bboxes: list,
        content_position: ContentPosition,
        start_lld: LogLineData
    ):
        first_content_col_bbox = content_col_bboxes[0]
        content_top = content_position.get_y_pos_start()
        content_top_adjusted = self._adjust_content_top(start_lld, content_top)
        if (content_top_adjusted > first_content_col_bbox.get_top()):
            first_content_col_bbox.set_top(content_top_adjusted)

    def _adjust_content_top(self, start_lld: LogLineData, content_top: int):
        if (self._is_item_header(start_lld) or
            self._is_prev_item_header(start_lld)):
            return content_top
        return content_top - self._layout_settings.get_baseline_skip_px()

    def _is_item_header(self, start_lld: LogLineData):
        item_index = start_lld.data_item_index
        item = self._ccs_data_store.get_main_text_item(item_index)
        return self._ccs_data_item_categorizer.is_header(item)

    def _is_prev_item_header(self, start_lld: LogLineData):
        prev_item_index = start_lld.data_item_index - 1
        prev_item = self._ccs_data_store.get_main_text_item(prev_item_index)
        if (prev_item is None): return False
        return self._ccs_data_item_categorizer.is_header(prev_item)

    def tune_last_content_col_bbox(
        self, content_col_bboxes: list, content_position: ContentPosition
    ):
        last_content_col_bbox = content_col_bboxes[-1]
        last_content_col_bbox.set_bottom(content_position.get_y_pos_end())
        self._tune_bbox_right(last_content_col_bbox, content_position)

    def _tune_bbox_right(
        self, content_col_bbox: Bbox, content_position: ContentPosition
    ):
        height = content_col_bbox.get_height()
        if not (height > self._layout_settings.get_baseline_skip_px()):
            content_col_bbox.set_right(content_position.get_x_pos_end())
