from data_loading.data_loader import DataLoader
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.stores.items_position_store import ItemsPositionStore
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.util.unit_converter import UnitConverter
from util import file_path_manager
from .paragraph_item_positions import ParagraphItemPositions

import re

class LogLine:
    def __init__(self, log_line: str):
        split = log_line.split(",,")
        self._mti_index = int(split[0])

        # ⚠️ Fix the crash here: remove non-digits from page number string
        raw_page = split[1].strip()
        cleaned_page = re.sub(r"[^\d]", "", raw_page)
        if not cleaned_page:
            raise ValueError(f"Invalid page number format: '{raw_page}'")

        self._page_num = int(cleaned_page)
        self._x_pos = int(split[2])
        self._y_pos = int(split[3])
        self._word = split[4].replace("\n", "")
        
    def get_mti_index(self) -> int:
        return self._mti_index

    def get_page_num(self) -> int:
        return self._page_num

    def get_x_pos(self) -> int:
        return self._x_pos
    
    def get_y_pos(self) -> int:
        return self._y_pos

    def get_word(self) -> str:
        return self._word

class ParagraphItemsPositionStore(ItemsPositionStore):
    """
    Loads the position information of every paragraph item in synthesized
    latex document from a log file and acts as store for this data.
    """

    _log_file_ext = "pwpos"

    def __init__(self, doc_file_path: str):
        super().__init__()
        log_file_path = file_path_manager.replace_file_extension(
            doc_file_path, ParagraphItemsPositionStore._log_file_ext)
        self.mti_index_list = []
        self._logs_to_data(log_file_path)

    def _logs_to_data(self, log_file_path: str):
        file_log_lines = DataLoader().load_file_as_lines(log_file_path)
        for file_log_line in file_log_lines:
            self._add_log_line_data_to_paragraph_pos_item(file_log_line)

    def _add_log_line_data_to_paragraph_pos_item(self, file_log_line: str):
        #a log line, is one line of the .pwpos file (in this case)
        #not a line of the syndocument
        log_line = LogLine(file_log_line)
        p_item_pos = self._get_or_create_item(log_line.get_mti_index())
        print(f'word {log_line.get_word()}')
        print(p_item_pos.get_first_word_y())
        if not (log_line.get_mti_index() in self.mti_index_list):
            page_height = Template().get_layout_settings().get_page_height_sp()
            font_size_pt = Template().get_layout_settings().get_font_size_as_int() + 1
            font_size_sp = UnitConverter().pt_to_sp(font_size_pt)
            p_item_pos.set_first_word_y(UnitConverter().sp_to_px(page_height - log_line.get_y_pos() - font_size_sp - 1))
            self.mti_index_list.append(log_line.get_mti_index())
            page_col_index = self._compute_page_col_index(log_line)
            p_item_pos.add_word_to_substring(
                log_line.get_page_num(), page_col_index, log_line.get_word())

    def _get_or_create_item(self, mti_index: int) -> ParagraphItemPositions:
        if (mti_index not in self.mti_index_list):
            print(f'creating new item with index {mti_index}')
            self._items[mti_index] = ParagraphItemPositions(mti_index)
        print(f'retrieved item at index {mti_index}')
        return self._items[mti_index]
    
    def get_or_none_item(self, mti_index: int) -> ParagraphItemPositions:
        if (mti_index not in self.mti_index_list):
            return None
        return self._items[mti_index]

    def _compute_page_col_index(self, log_line: LogLine) -> int:
        x_pos = UnitConverter().sp_to_px(log_line.get_x_pos())
        layout_settings = Template().get_layout_settings()
        page_col_bboxes = layout_settings.get_page_cols_bboxes(
            log_line.get_page_num())
        for index, page_col_bbox in enumerate(page_col_bboxes):
            if (page_col_bbox.includes_x_pos(x_pos)):
                return index
            if (x_pos < (page_col_bbox.get_right() + layout_settings.get_col_sep_px()) - 1):
                return index
        assert False # A column bbox must be found.
