from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData
from synthetic_data_generation.templates.template import Template

class PosLogsCorrector:

    def __init__(self):
        self._layout_settings = Template().get_layout_settings()

    def correct_pos_logs(self, raw_log_lines: list):
        self._raw_log_lines = raw_log_lines
        self._corrected_log_lines = []
        self._end_log_line_store = {}
        self._raw_log_line_index = 0
        limit = len(self._raw_log_lines) - 1
        while (self._raw_log_line_index < limit):
            self._insert_correct_log_lines()
            self._raw_log_line_index += 1
        self._add_correct_log_line(LogLineData(self._raw_log_lines[-1]))
        print('finished inserting correct pos logs')
        return self._corrected_log_lines

    def _insert_correct_log_lines(self):
        lld = LogLineData(self._raw_log_lines[self._raw_log_line_index])
        next_lld = LogLineData(
            self._raw_log_lines[self._raw_log_line_index + 1])
        if (self._was_lld_used_to_close_start_lld_artificially(lld)): return
        if (self._is_reading_order_distorted(lld, next_lld)):
            self._handle_reading_order_distortion(lld, next_lld)
        else:
            self._add_correct_log_line(lld)

    def _handle_reading_order_distortion(
        self, lld: LogLineData, next_lld: LogLineData):
        if (self._was_lld_used_to_close_start_lld_artificially(next_lld)):
            self._add_correct_log_line(lld)
        else:
            insert_log_line = self._gen_insert_ll(lld, next_lld)
            self._add_correct_log_line(lld)
            self._add_correct_log_line(insert_log_line)
            self._update_end_log_line_store(insert_log_line)

    def _update_end_log_line_store(self, lld: LogLineData):
        if not (lld.is_start_log_line):
            self._end_log_line_store[lld.data_item_index] = lld

    def _add_correct_log_line(self, lld: LogLineData):
        self._corrected_log_lines.append(lld.to_str() + "\n")

    def _was_lld_used_to_close_start_lld_artificially(self, lld: LogLineData):
        return (not (lld.is_start_log_line) and
            (lld.data_item_index in self._end_log_line_store) and
            (lld.page_num ==
            self._end_log_line_store[lld.data_item_index].page_num))

    def _is_reading_order_distorted(
        self, lld: LogLineData, next_lld: LogLineData
    ) -> bool:
        if (lld.is_start_log_line):
            return self._next_item_does_not_end_current_item(next_lld)
        return self._next_item_does_not_start_new_item(next_lld)

    def _next_item_does_not_end_current_item(
        self, next_lld: LogLineData
    ) -> bool:
        return next_lld.is_start_log_line
    
    def _next_item_does_not_start_new_item(
        self, next_lld: LogLineData
    ) -> bool:
        return not next_lld.is_start_log_line

    def _gen_insert_ll(
        self, lld: LogLineData, next_lld: LogLineData
    ) -> LogLineData:
        if (lld.is_start_log_line):
            return self._gen_artificial_end_log_line(lld)
        return self._gen_artificial_start_log_line(lld, next_lld)

    def _gen_artificial_start_log_line(
        self, lld: LogLineData, next_lld: LogLineData
    ) -> LogLineData:
        art_slld = LogLineData(next_lld.to_str())
        art_slld.is_start_log_line = True
        art_slld.page_num = lld.page_num
        art_slld.xpos = (self._layout_settings.get_page_text_x_origin_sp(
            lld.page_num))
        art_slld.ypos = lld.ypos
        return art_slld

    def _gen_artificial_end_log_line(self, lld: LogLineData) -> LogLineData:
        art_elld = LogLineData(lld.to_str())
        art_elld.is_start_log_line = False
        end_lld = self._find_end_log_line_for_start_log_line(lld)
        (xpos, ypos) = self._get_pos_coordinates_for_art_end_log_line(
            lld, end_lld)
        art_elld.xpos = xpos
        art_elld.ypos = ypos
        return art_elld

    def _find_end_log_line_for_start_log_line(
        self, start_lld: LogLineData
    ) -> LogLineData:
        scan_index = self._raw_log_line_index + 1
        while scan_index < len(self._raw_log_lines):
            index_lld = LogLineData(self._raw_log_lines[scan_index])
            if index_lld.data_item_index == start_lld.data_item_index:
                return index_lld
            scan_index += 1

        # If we fall out of the loop, log and return a fallback
        print(f"[WARNING] No matching end log line found for start: {start_lld}")
        return start_lld  # Or return None and handle accordingly

    def _get_pos_coordinates_for_art_end_log_line(
        self, start_lld: LogLineData, end_lld: LogLineData
    ) -> tuple[int, int]:
        if (start_lld.page_num == end_lld.page_num):
            return (end_lld.xpos, end_lld.ypos)
        xpos = self._layout_settings.get_page_text_x_end_sp(start_lld.page_num)
        ypos = (self._layout_settings.get_page_height_sp() -
            self._layout_settings.get_text_y_end_sp())
        return (xpos, ypos)
