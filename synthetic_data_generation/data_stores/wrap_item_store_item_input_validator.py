from util.latex_item_type_names import LatexItemTypeNames

class WrapItemStoreItemInputValidator:

    _valid_latex_item_categories = [
        LatexItemTypeNames.CAPTION,
        LatexItemTypeNames.FIGURE,
        LatexItemTypeNames.TABLE
    ]
    _valid_latex_item_wrap_positions = ["", "r", "l"]

    def is_input_valid(
        latex_item_category: str,
        latex_item_wrap_position: str,
        latex_item_wrap_line_width: float
    ) -> bool:
        if (WrapItemStoreItemInputValidator.
            _is_latex_item_category_invalid(latex_item_category)):
            return False
        if (WrapItemStoreItemInputValidator.
            _is_latex_item_wrap_position_invalid(latex_item_wrap_position)):
            return False
        return not (WrapItemStoreItemInputValidator.
            _is_latex_item_wrap_line_width_invalid(latex_item_wrap_line_width))

    def _is_latex_item_category_invalid(latex_item_category: str):
        return (latex_item_category not in
            WrapItemStoreItemInputValidator._valid_latex_item_categories)

    def _is_latex_item_wrap_position_invalid(wrap_position: str):
        return (wrap_position not in
            WrapItemStoreItemInputValidator._valid_latex_item_wrap_positions)

    def _is_latex_item_wrap_line_width_invalid(line_width: float):
        return (line_width < 0 or line_width > 1.0)
