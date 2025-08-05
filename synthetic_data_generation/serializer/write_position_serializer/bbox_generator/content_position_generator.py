from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.util.unit_converter import UnitConverter
from .content_position import ContentPosition

class ContentPositionGenerator:

    def __init__(self):
        self._layout_settings = Template().get_layout_settings()
        self._unit_converter = UnitConverter()

    def gen_one_page_content_position(
        self, start_lld: LogLineData, end_lld: LogLineData
    ):
        x_start = self._sp_to_px(start_lld.xpos)
        y_start = self._latex_y_to_page_image_y(self._sp_to_px(start_lld.ypos))
        x_end = self._sp_to_px(end_lld.xpos)
        y_end = self._latex_y_to_page_image_y(self._sp_to_px(end_lld.ypos))
        return ContentPosition(x_start, y_start, x_end, y_end)

    def gen_first_page_content_position(self, start_lld: LogLineData):
        x_start = self._sp_to_px(start_lld.xpos)
        y_start = self._latex_y_to_page_image_y(self._sp_to_px(start_lld.ypos))
        x_end = self._layout_settings.get_page_text_x_end_px(
            start_lld.page_num)
        y_end = self._layout_settings.get_text_y_end_px()
        return ContentPosition(x_start, y_start, x_end, y_end)

    def gen_last_page_content_position(self, end_lld: LogLineData):
        x_start = self._layout_settings.get_page_text_x_origin_px(
            end_lld.page_num)
        y_start = self._layout_settings.get_text_y_origin_px()
        x_end = self._sp_to_px(end_lld.xpos)
        y_end = self._latex_y_to_page_image_y(self._sp_to_px(end_lld.ypos))
        return ContentPosition(x_start, y_start, x_end, y_end)

    def gen_middle_page_content_position(self, page_num: int):
        x_start = self._layout_settings.get_page_text_x_origin_px(page_num)
        y_start = self._layout_settings.get_text_y_origin_px()
        x_end = self._layout_settings.get_page_text_x_end_px(page_num)
        y_end = self._layout_settings.get_text_y_end_px()
        return ContentPosition(x_start, y_start, x_end, y_end)

    def _latex_y_to_page_image_y(self, latex_y_coordinate):
        return (self._layout_settings.get_page_height_px() -
            latex_y_coordinate)

    def _sp_to_px(self, value):
        return self._unit_converter.sp_to_px(value)
