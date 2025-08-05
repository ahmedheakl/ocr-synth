from synthetic_data_generation.data_item_generation.data_items.main_text_item import MainTextItem
from synthetic_data_generation.data_item_generation.data_items.util.prov import Prov
from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.data_stores.main_text_item_store import MainTextItemStore
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.bbox_generator import BboxGenerator
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.line_num_bbox_generator import LineNumBboxGenerator
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.items_position_stores_manager import ItemsPositionStoresManager
from synthetic_data_generation.templates.template import Template
from util.latex_item_type_names import LatexItemTypeNames
from .ground_truth_item_line_nums import GroundTruthItemLineNums
from .log_line_data import LogLineData
from .segment import Segment

class GroundTruthItem:

    def __init__(self, start_log_line: str, end_log_line: str):
        slld = LogLineData(start_log_line)
        elld = LogLineData(end_log_line)
        self._start_latex_page_num = slld.page_num
        self._end_latex_page_num = elld.page_num
        self._main_text_item = MainTextItemStore().get_item(
            slld.data_item_index)
        print("main item ref type ", self._main_text_item._ref_type)
        if self._main_text_item._ref_type == 'tables':
            print('entering bboxGenerator table')
            bboxes = BboxGenerator().log_lines_to_bboxes(slld, elld, is_table=True)
        bboxes = BboxGenerator().log_lines_to_bboxes(slld, elld)
        self._prov = self._gen_prov(bboxes)
        self._line_nums = self._gen_line_nums(bboxes)

    def get_index(self) -> int:
        return self._main_text_item.get_index()

    def get_start_latex_page_num(self) -> int:
        return self._start_latex_page_num

    def get_end_latex_page_num(self) -> int:
        return self._end_latex_page_num

    def is_spread_across_multiple_latex_pages(self) -> bool:
        return self._start_latex_page_num != self._end_latex_page_num

    def is_list_item(self) -> bool:
        return self._main_text_item.is_list_item()

    def get_type(self) -> str:
        return self._main_text_item.get_type()

    def get_prov(self):
        return self._prov

    def get_prov_item(self, index: int):
        return self._prov.get_item(index)

    def get_line_nums(self) -> GroundTruthItemLineNums:
        return self._line_nums

    def append(self, item):
        self._append_main_text_item_bboxes(item)
        self._append_line_nums_bboxes(item)

    def _append_main_text_item_bboxes(self, item):
        self._prov.extend(item.get_prov().get_items())

    def _append_line_nums_bboxes(self, item):
        this_line_nums_prov = self._line_nums.get_prov()
        other_line_nums_prov = item.get_line_nums().get_prov()
        this_line_nums_prov.extend(other_line_nums_prov.get_items())

    def to_reading_order_format(self) -> list[dict]:
        if (Template().get_line_nums_settings().are_in_ro()):
            return [
                self._gen_item_line_nums_reading_order_format(),
                self._gen_item_content_reading_order_format()
            ]
        return [self._gen_item_content_reading_order_format()]

    def to_segments(
        self,
        next_segment_index: int,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> list[Segment]:
        segment_index = next_segment_index
        segments = []
        line_num_prov_items = (self._line_nums.get_prov().
            get_items_sorted_by_page_num())
        item_prov_items = (self._prov.
            get_items_sorted_by_page_num())
        for page_num in sorted(item_prov_items.keys()):
            if (page_num in line_num_prov_items.keys()):
                for prov_item in line_num_prov_items[page_num]:
                    segments.append(self._gen_line_num_segment(
                        segment_index, prov_item, pos_stores_manager))
                    segment_index += 1
            for prov_item in item_prov_items[page_num]:
                segments.append(self._gen_main_text_item_segment(
                    segment_index, prov_item, pos_stores_manager))
                segment_index += 1
        return segments

    def _gen_line_num_segment(
        self,
        segment_index: int,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> Segment:
        return Segment(
            segment_index,
            self._gen_line_num_dummy_main_text_item(),
            prov_item,
            pos_stores_manager
        )

    def _gen_line_num_dummy_main_text_item(self) -> MainTextItem:
        return MainTextItem(
            index=None,
            data={
                "label": LatexItemTypeNames.LINE_NUM,
                "prov": [],
                "text": "",
                "type": "texts"
            }
        )

    def _gen_main_text_item_segment(
        self,
        segment_index: int,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> Segment:
        return Segment(
            segment_index,
            self._main_text_item,
            prov_item,
            pos_stores_manager)

    def _gen_item_line_nums_reading_order_format(self) -> dict:
        return self._line_nums.to_reading_order_format()
    
    def retrieve_children_items_if_group(self) -> list:
        types = self._main_text_item.get_self_ref_type()
        if types != 'groups':
            return None
        return self._main_text_item.get_children_item()

    def _gen_item_content_reading_order_format(self) -> dict:
        types =  self._main_text_item.get_self_ref_type()
        if types == 'texts':
            return {
                "self_ref": self._main_text_item.get_self_ref_type(),
                "parent": {'$ref': ""},
                "children": [],
                "content_layer": "furniture",
                "label": self._main_text_item.get_type(),
                "prov": self._prov.to_list_of_dicts(),
                "orig": self._main_text_item.get_text(),
                "text": self._main_text_item.get_text(),
            }
        elif types == 'pictures':
            return {
                "self_ref": self._main_text_item.get_self_ref_type(),
                "parent": {'$ref': ""},
                "children": [],
                "content_layer": "furniture",
                "label": self._main_text_item.get_type(),
                "prov": self._prov.to_list_of_dicts(),
                "captions": [],
                "references": [],
                "footnotes": [],
                "image": {"mimetype": "image/png",
                          "dpi": 150,
                          "size": self._main_text_item.get_image_size(),
                          "uri": "" 
                        },
                "annotations": self._main_text_item.get_annotations()
            }
        elif types == 'tables':
            return {
                "self_ref": self._main_text_item.get_self_ref_type(),
                "parent": {'$ref': ""},
                "children": [],
                "content_layer": "furniture",
                "label": self._main_text_item.get_type(),
                "prov": self._prov.to_list_of_dicts(),
                "captions": [],
                "references": [],
                "footnotes": [],
                "data": self._main_text_item.get_table_data_dict(),
            }
        elif types == 'groups':
            return {
                "self_ref": self._main_text_item.get_self_ref_type(),
                "parent": {'$ref': ""},
                "children": {},
                "content_layer": "furniture",
                "name": "group",
                "prov": self._prov.to_list_of_dicts(),
                "label": self._main_text_item.get_type(),
            }
        else:
            return {
                "self_ref": self._main_text_item.get_self_ref_type(),
                "parent": {'$ref': ""},
                "children": [],
                "content_layer": "furniture",
                "label": self._main_text_item.get_type(),
                "prov": self._prov.to_list_of_dicts(),
                "orig": self._main_text_item.get_text(),
                "text": self._main_text_item.get_text(),
            }

    def _gen_line_nums(
        self, item_bboxes: list[Bbox]
    ) -> GroundTruthItemLineNums:
        line_num_bboxes = (LineNumBboxGenerator().
            gen_line_num_bboxes_for_main_text_item(
                self._main_text_item.get_type(), item_bboxes))
        return GroundTruthItemLineNums(line_num_bboxes)

    def _gen_prov(self, bboxes: list[Bbox]) -> Prov:
        return Prov([bbox.to_prov_item_dict() for bbox in bboxes])
