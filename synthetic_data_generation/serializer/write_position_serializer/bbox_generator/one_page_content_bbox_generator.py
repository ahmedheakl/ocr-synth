from synthetic_data_generation.data_stores.wrap_items_store import WrapItemsStore
from synthetic_data_generation.data_stores.main_text_item_store import MainTextItemStore
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_position import ContentPosition
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.page_content_bbox_generator import PageContentBbboxGenerator
from util.data_stores.docling_data_store import DoclingDataStore
from util.latex_item_type_names import LatexItemTypeNames
from .wrapable_item_bbox_generator import wrapable_item_bbox_generator_table

class OnePageContentBboxGenerator(PageContentBbboxGenerator):

    def gen_bboxes(self, start_lld: LogLineData, end_lld: LogLineData) -> list:
        content_position = (self._content_pos_generator.
            gen_one_page_content_position(start_lld, end_lld))
        if (self._is_page_wide_item(start_lld, content_position)):
            print('is page wide item')
            return [self._gen_page_width_bbox(start_lld, content_position)]
        return self._gen_col_bboxes(start_lld, content_position)

    def _is_page_wide_item(
        self, start_lld: LogLineData, content_position: ContentPosition
    ) -> bool:
        item = MainTextItemStore().get_item(start_lld.data_item_index)
        label = item._type
        if label == 'table':
            return True
        if not (self._can_item_be_page_wide(start_lld)):
            print('cannot be wide')
            return False
        return self._is_content_positioned_above_page_cols(
            start_lld.page_num, content_position)

    def _can_item_be_page_wide(self, lld: LogLineData) -> bool:
        ccs_item = MainTextItemStore().get_item(lld.data_item_index)
        ccs_item_type = ccs_item._type
        print('label ', ccs_item_type)
        return (ccs_item_type == LatexItemTypeNames.FIGURE or
            ccs_item_type == LatexItemTypeNames.CAPTION or
            ccs_item_type == LatexItemTypeNames.TABLE)

    def _is_content_positioned_above_page_cols(
        self, page_num: int, content_position: ContentPosition
    ):
        content_col_bboxes_top = (self._doc_pages_col_bboxes_store.
            get_or_create_page_col_bboxes(page_num)[0].get_top())
        return content_position.get_y_pos_start() < content_col_bboxes_top

    def _gen_page_width_bbox(
        self,
        start_lld: LogLineData,
        content_position: ContentPosition
    ) -> Bbox:
        layout_settings = Template().get_layout_settings()
        coordinates = [
            layout_settings.get_page_text_x_origin_px(start_lld.page_num),
            content_position.get_y_pos_start(),
            layout_settings.get_page_text_x_end_px(start_lld.page_num),
            content_position.get_y_pos_end()
        ]
        return Bbox(coordinates, start_lld.page_num)

    def _gen_col_bboxes(
        self, lld: LogLineData, content_position: ContentPosition
    ) -> list:
        if (WrapItemsStore().has_item_of_index(lld.data_item_index)):
            return [self._gen_wrap_item_bbox(lld, content_position)]
        return self._gen_regular_item_bboxes(lld, content_position)

    def _gen_wrap_item_bbox(
        self,
        lld: LogLineData,
        content_position: ContentPosition
    ) -> Bbox:
        item = WrapItemsStore().get_item_by_index(lld.data_item_index)
        generator = wrapable_item_bbox_generator_table.get_bbox_generator(
            item.get_latex_item_category())
        return generator.gen_bbox(lld, content_position)

    def _gen_regular_item_bboxes(
        self,
        lld: LogLineData,
        content_position: ContentPosition
    ) -> list:
        bboxes = self._get_content_col_bboxes(
            lld.page_num, content_position)
        self._content_col_bbox_tuner.tune_first_content_col_bbox(
            bboxes, content_position, lld)
        self._content_col_bbox_tuner.tune_last_content_col_bbox(
            bboxes, content_position)
        return bboxes
