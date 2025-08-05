from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.page_content_bbox_generator import PageContentBbboxGenerator
from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData

class MultiPageContentBboxGenerator(PageContentBbboxGenerator):

    def gen_bboxes(self, start_lld: LogLineData, end_lld: LogLineData) -> list:
        if (self._is_content_on_two_pages(start_lld, end_lld)):
            return self._gen_two_page_content_bboxes(start_lld, end_lld)
        return self._gen_multi_page_content_bboxes(start_lld, end_lld)

    def _is_content_on_two_pages(
        self, start_lld: LogLineData, end_lld: LogLineData
    ):
        return ((start_lld.page_num + 1) == end_lld.page_num)

    def _gen_two_page_content_bboxes(
        self, start_lld: LogLineData, end_lld: LogLineData
    ) -> list:
        return (self._gen_first_page_content_bboxes(start_lld) +
            self._gen_last_page_content_bboxes(end_lld))

    def _gen_multi_page_content_bboxes(
        self, start_lld: LogLineData, end_lld: LogLineData
    ) -> list:
        return (self._gen_first_page_content_bboxes(start_lld) +
            self._gen_middle_pages_content_bboxes(start_lld, end_lld) +
            self._gen_last_page_content_bboxes(end_lld))

    def _gen_first_page_content_bboxes(self, start_lld: LogLineData) -> list:
        content_position = (self._content_pos_generator.
            gen_first_page_content_position(start_lld))
        content_col_bboxes = self._get_content_col_bboxes(
            start_lld.page_num, content_position)
        self._content_col_bbox_tuner.tune_first_content_col_bbox(
            content_col_bboxes, content_position, start_lld)
        return content_col_bboxes

    def _gen_last_page_content_bboxes(self, end_lld: LogLineData) -> list:
        content_position = (self._content_pos_generator.
            gen_last_page_content_position(end_lld))
        content_col_bboxes = self._get_content_col_bboxes(
            end_lld.page_num, content_position)
        self._content_col_bbox_tuner.tune_last_content_col_bbox(
            content_col_bboxes, content_position)
        return content_col_bboxes

    def _gen_middle_pages_content_bboxes(
        self, start_lld: LogLineData, end_lld: LogLineData
    ) -> list:
        middle_pages_bboxes = []
        first_middle_page_num = start_lld.page_num + 1
        last_page_num = end_lld.page_num
        for middle_page_num in range(first_middle_page_num, last_page_num):
            middle_pages_bboxes += self._gen_middle_page_content_bboxes(
                middle_page_num)
        return middle_pages_bboxes

    def _gen_middle_page_content_bboxes(self, page_num: int) -> list:
        content_position = (self._content_pos_generator.
            gen_middle_page_content_position(page_num))
        return self._get_content_col_bboxes(page_num, content_position)
