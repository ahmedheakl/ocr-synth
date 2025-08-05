from synthetic_data_generation.data_stores.wrap_items_store import WrapItemsStore
from synthetic_data_generation.data_stores.wrap_item_store_item import WrapItemStoreItem
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_position import ContentPosition
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData
from synthetic_data_generation.templates.template import Template
from util.latex_item_type_names import LatexItemTypeNames
from .wrapable_item_bbox_generator import WrapableItemBboxGenerator

class WrapableTableItemBbboxGenerator(WrapableItemBboxGenerator):

    def gen_bbox(
        self, lld: LogLineData, content_position: ContentPosition
    ) -> Bbox:
        coordinates = self._compute_bbox_coordinates(lld, content_position)
        return Bbox(coordinates, lld.page_num)

    def _compute_bbox_coordinates(
        self, lld: LogLineData, content_position: ContentPosition
    ) -> list:
        (left, right) = self._compute_h_bbox_bounds(lld, content_position)
        coordinates = [
            left,
            content_position.get_y_pos_start(),
            right,
            content_position.get_y_pos_end()
        ]
        return coordinates

    def _compute_h_bbox_bounds(
        self, lld: LogLineData, content_position: ContentPosition
    ) -> tuple[int, int]:
        item = WrapItemsStore().get_item(
            LatexItemTypeNames.TABLE, lld.data_item_index)
        if (item.is_wrap_pos_left()):
            return self._compute_wrap_pos_left_h_bbox_bounds(
                content_position, lld.page_num, item)
        return self._compute_wrap_pos_right_h_bbox_bounds(
            content_position, lld.page_num, item)

    def _compute_wrap_pos_left_h_bbox_bounds(
        self,
        content_position: ContentPosition,
        page_num: int,
        item: WrapItemStoreItem
    ) -> tuple[int, int]:
        featured_col_bbox = self._get_page_col_bbox_for_content_position(
            content_position, page_num)
        layout_settings = Template().get_layout_settings()
        col_width = layout_settings.get_col_width_px()
        left = featured_col_bbox.get_left()
        right = (featured_col_bbox.get_left() +
            col_width * item.get_latex_item_wrap_line_width())
        return (left, right)

    def _compute_wrap_pos_right_h_bbox_bounds(
        self,
        content_position: ContentPosition,
        page_num: int,
        item: WrapItemStoreItem
    ) -> tuple[int, int]:
        featured_col_bbox = self._get_page_col_bbox_for_content_position(
            content_position, page_num)
        layout_settings = Template().get_layout_settings()
        col_width = layout_settings.get_col_width_px()
        left = (featured_col_bbox.get_left() +
            col_width * (1.0 - item.get_latex_item_wrap_line_width()))
        right = featured_col_bbox.get_right()
        return (left, right)
