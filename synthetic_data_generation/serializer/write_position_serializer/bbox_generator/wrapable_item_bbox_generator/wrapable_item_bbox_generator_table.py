from .wrapable_caption_item_bbox_generator import WrapableCaptionItemBboxGenerator
from .wrapable_figure_item_bbox_generator import WrapableFigureItemBboxGenerator
from .wrapable_table_item_bbox_generator import WrapableTableItemBbboxGenerator
from util.latex_item_type_names import LatexItemTypeNames

_latex_item_type_to_bbox_generator = {
    LatexItemTypeNames.CAPTION: WrapableCaptionItemBboxGenerator,
    LatexItemTypeNames.FIGURE: WrapableFigureItemBboxGenerator,
    LatexItemTypeNames.TABLE: WrapableTableItemBbboxGenerator
}

def get_bbox_generator(category: str):
    if (category in _latex_item_type_to_bbox_generator):
        generator_class = _latex_item_type_to_bbox_generator[category]
        return generator_class()
    return None
