from .table_item_row_position import TableItemRowPosition

class TableItemPositions:

    def __init__(self):
        self._row_positions = {} # row_index: <TableItemRowPosition>

    def add_row_position(self, position: TableItemRowPosition):
        self._row_positions[position.get_row_index()] = position

    def get_row_positions_of_page(
        self, page_num: int
    ) -> list[TableItemRowPosition]:
        rows = []
        for _, row_position in sorted(self._row_positions.items()):
            if (row_position.get_page_num() == page_num):
                rows.append(row_position)
        return rows

    def get_last_row_of_page(self, page_num: int) -> TableItemRowPosition:
        for _, row_position in sorted(self._row_positions.items(), reverse=True):
            if (row_position.get_page_num() == page_num):
                return row_position

    def get_page_num_last(self) -> int:
        row_index_max = sorted(self._row_positions.keys())[-1]
        last_row = self._row_positions[row_index_max]
        return last_row.get_page_num()
