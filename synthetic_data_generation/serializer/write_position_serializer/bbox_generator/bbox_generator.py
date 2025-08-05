from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.one_page_content_bbox_generator import OnePageContentBboxGenerator
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.multi_page_content_bbox_generator import MultiPageContentBboxGenerator

class BboxGenerator:

    def log_lines_to_bboxes(
        self, start_lld: LogLineData, end_lld: LogLineData, is_table = False
    ) -> list:
        if (self._is_content_on_one_page(start_lld, end_lld, is_table)):
            return OnePageContentBboxGenerator().gen_bboxes(start_lld, end_lld)
        return MultiPageContentBboxGenerator().gen_bboxes(start_lld, end_lld)

    def _is_content_on_one_page(
        self, start_lld: LogLineData, end_lld: LogLineData, is_table: bool
    ):
        return start_lld.page_num == end_lld.page_num
