from synthetic_data_generation.data_stores.wrap_item_store_item_input_validator import WrapItemStoreItemInputValidator

class WrapItemStoreItem:

    def __init__(self,
        latex_item_category: str,
        latex_item_index: int,
        latex_item_wrap_position: str,
        latex_item_wrap_line_width: float
    ):
        assert WrapItemStoreItemInputValidator.is_input_valid(
            latex_item_category, latex_item_wrap_position,
            latex_item_wrap_line_width)
        self._latex_item_category = latex_item_category
        self._latex_item_index = latex_item_index
        self._latex_item_wrap_position = latex_item_wrap_position
        self._latex_item_wrap_line_width = latex_item_wrap_line_width

    def get_latex_item_index(self) -> int:
        return self._latex_item_index

    def get_latex_item_category(self) -> str:
        return self._latex_item_category

    def get_latex_item_wrap_position(self) -> str:
        return self._latex_item_wrap_position

    def get_latex_item_wrap_line_width(self) -> float:
        return self._latex_item_wrap_line_width

    def is_wrap_pos_left(self) -> bool:
        return str.lower(self._latex_item_wrap_position) == "l"

    def is_wrap_pos_right(self) -> bool:
        return str.lower(self._latex_item_wrap_position) == "r"
