from synthetic_data_generation.data_item_generation.data_items.util.prov import Prov
from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox

class GroundTruthItemLineNums:

    _name = "line-numbers"
    _type = _name

    def __init__(self, line_num_bboxes: list[Bbox]):
        self._prov = Prov([bbox.to_prov_item_dict() for bbox in line_num_bboxes])

    def get_prov(self) -> Prov:
        return self._prov

    def to_reading_order_format(self) -> list[dict]:
        return {
            "self_ref": "",
            "parent": {'$ref': ""},
            "children": [],
            "content_layer": "furniture",
            "label": GroundTruthItemLineNums._type,
            "prov": self._prov.to_list_of_dicts(),
            "prov":self._prov.to_list_of_dicts(),
            "text": GroundTruthItemLineNums._name,
        }