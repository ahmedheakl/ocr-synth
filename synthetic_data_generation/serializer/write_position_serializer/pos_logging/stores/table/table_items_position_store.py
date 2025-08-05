from data_loading.data_loader import DataLoader
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.stores.items_position_store import ItemsPositionStore
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.util.unit_converter import UnitConverter
from util import file_path_manager
from .table_item_positions import TableItemPositions
from .table_item_row_position import TableItemRowPosition

class TableItemsPositionStore(ItemsPositionStore):

    _log_file_ext = "trpos"

    def __init__(self, doc_file_path: str):
        super().__init__()
        log_file_path = file_path_manager.replace_file_extension(
            doc_file_path, TableItemsPositionStore._log_file_ext)
        self._items = self._logs_to_data(log_file_path)

    def _logs_to_data(self, log_file_path: str) -> dict:
        data = {}
        log_lines = DataLoader().load_file_as_lines(log_file_path)
        for log_line in log_lines:
            row_position = self._log_line_to_row_position(log_line)
            table_item_index = row_position.get_table_item_index()
            if (table_item_index not in data):
                data[table_item_index] = TableItemPositions()
            data[table_item_index].add_row_position(row_position)
        return data

    def _log_line_to_row_position(self, log_line: str) -> TableItemRowPosition:
        split = log_line.split(",,")
        table_item_index = int(split[0])
        page_num = int(split[1])
        row_index = int(split[2])
        left = UnitConverter().sp_to_px(int(split[3]))
        page_height = Template().get_layout_settings().get_page_height_sp()
        top = UnitConverter().sp_to_px(page_height - int(split[4]))
        return TableItemRowPosition(
            table_item_index, page_num, row_index, left, top)
