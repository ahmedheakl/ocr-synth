from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_position import ContentPosition
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox
from synthetic_data_generation.templates.template import Template

class WrapableItemBboxGenerator:

    def _get_page_col_bbox_for_content_position(
        self, content_position: ContentPosition, page_num: int
    ) -> Bbox:
        layout_settings = Template().get_layout_settings()
        page_cols_bboxes = layout_settings.get_page_cols_bboxes(page_num)
        for page_col_bbox in page_cols_bboxes:
            if (content_position.is_located_in_bbox(page_col_bbox)):
                return page_col_bbox
