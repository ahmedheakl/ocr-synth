from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_col_bbox_tuner import ContentColBboxTuner
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_position import ContentPosition
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.content_position_generator import ContentPositionGenerator
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.doc_pages_col_bboxes_store import DocPagesColBboxesStore
from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox

class PageContentBbboxGenerator:
    """
    Abstract parent class for the bbox generators that deal with content that
    is either rendered on a single page or on multiple pages.
    """

    def __init__(self):
        self._content_col_bbox_tuner = ContentColBboxTuner()
        self._content_pos_generator = ContentPositionGenerator()
        self._doc_pages_col_bboxes_store = DocPagesColBboxesStore()

    def _get_content_col_bboxes(
        self, page_num: int, content_position: ContentPosition
    ) -> list:
        page_col_bboxes = (self._doc_pages_col_bboxes_store.
            get_or_create_page_col_bboxes(page_num))
        return self._select_content_col_bboxes_from_page_col_bboxes(
            page_col_bboxes, content_position)

    def _select_content_col_bboxes_from_page_col_bboxes(
        self, page_col_bboxes: list, content_position: ContentPosition
    ) -> list:
        content_col_bboxes = []
        for page_col_bbox in page_col_bboxes:
            if (self._is_content_in_page_col(page_col_bbox, content_position)):
                content_col_bboxes.append(page_col_bbox)
        return content_col_bboxes

    def _is_content_in_page_col(
        self, page_col_bbox: Bbox, content_position: ContentPosition
    ):
        is_content_to_the_left_of_col = (
            page_col_bbox.get_left() > content_position.get_x_pos_end())
        is_content_to_the_right_of_col = (
            page_col_bbox.get_right() < content_position.get_x_pos_start())
        is_content_outside_of_col = (
            is_content_to_the_left_of_col or is_content_to_the_right_of_col)
        return not is_content_outside_of_col
