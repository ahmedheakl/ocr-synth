from synthetic_data_generation.data_item_generation.data_items.main_text_item import MainTextItem
from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.items_position_stores_manager import ItemsPositionStoresManager

class Segment:

    def __init__(
        self,
        index: int,
        main_text_item: MainTextItem,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ):
        self._index = index
        self._label = main_text_item.get_label()
        self._page_num = prov_item.get_page_num()
        self._bbox = prov_item.get_bbox_normalized()
        self._data = main_text_item.get_segment_data(
            prov_item, pos_stores_manager)
        self._text = main_text_item.get_segment_text(
            prov_item, pos_stores_manager)
        self._has_text_break = main_text_item.has_text_break(
            prov_item, pos_stores_manager)
        self._has_page_break = main_text_item.has_page_break(
            prov_item, pos_stores_manager)

    def get_index(self) -> int:
        return self._index

    def get_page_num(self) -> int:
        return self._page_num

    def to_dict(self) -> dict:
        segment = {
            "bbox": self._bbox,
            "data": self._data,
            "index_in_doc": self._index,
            "label": self._label,
            "text": self._text
        }
        if (self._has_text_break):
            segment["has_text_break"] = True
        if (self._has_page_break):
            segment["has_page_break"] = True
        return segment
