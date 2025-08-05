from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_position import ContentPosition
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.serializer.write_position_serializer.data_structures.log_line_data import LogLineData
from .wrapable_item_bbox_generator import WrapableItemBboxGenerator

class WrapableFigureItemBboxGenerator(WrapableItemBboxGenerator):

    def gen_bbox(
        self, lld: LogLineData, content_position: ContentPosition
    ) -> Bbox:
        return Bbox(content_position.to_bbox_coordinates(), lld.page_num)
