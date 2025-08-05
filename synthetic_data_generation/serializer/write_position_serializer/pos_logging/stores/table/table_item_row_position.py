class TableItemRowPosition:

    def __init__(
        self,
        table_item_index: int,
        page_num: int,
        row_index: int,
        left: int,
        top: int
    ):
        self._table_item_index = table_item_index
        self._page_num = page_num
        self._row_index = row_index
        self._left = left # [px]
        self._top = top # [px]

    def get_table_item_index(self) -> int:
        return self._table_item_index

    def get_page_num(self) -> int:
        return self._page_num

    def get_row_index(self) -> int:
        return self._row_index

    def get_position(self) -> tuple[int, int]:
        return (self._left, self._top)
