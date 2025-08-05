from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_data import GroundTruthData
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_item import GroundTruthItem
from synthetic_data_generation.serializer.write_position_serializer.bbox_optimizer.bbox_separator import BboxSeparator
from util.latex_item_type_names import LatexItemTypeNames

class DocumentItemsBboxSeparator:

    def separate_item_bboxes_from_other_items(
        self,
        item: GroundTruthItem,
        gt_data: GroundTruthData,
        page_images: list
    ):
        if (self._item_bbox_intersects_with_other_items(item, gt_data)):
            self._separate_item_bboxes_from_other_items(item, page_images)

    def _item_bbox_intersects_with_other_items(
        self, item: GroundTruthItem, data: GroundTruthData
    ):
        return (item.is_spread_across_multiple_latex_pages() or
            self._is_prev_item_figure(item, data) or
            self._is_prev_item_table(item, data))

    def _is_prev_item_figure(
        self, item: GroundTruthItem, data: GroundTruthData
    ):
        prev_item_index = item.get_index() - 1
        prev_item = data.get_item(prev_item_index)
        if (prev_item is None): return False
        return prev_item.get_type() == LatexItemTypeNames.FIGURE

    def _is_prev_item_table(
        self, item: GroundTruthItem, data: GroundTruthData
    ):
        prev_item_index = item.get_index() - 1
        prev_item = data.get_item(prev_item_index)
        if (prev_item is None): return False
        return prev_item.get_type() == LatexItemTypeNames.TABLE

    def _separate_item_bboxes_from_other_items(
        self, item: GroundTruthItem, page_images: list
    ):
        prov_items = item.get_prov().get_items()
        for prov_item in prov_items:
            self._separate_item_bbox_from_other_items(prov_item, page_images)

    def _separate_item_bbox_from_other_items(
        self, prov_item: ProvItem, page_images: list
    ):
        bbox = prov_item.get_bbox()
        page_index = prov_item.get_page_num() - 1
        page_image = page_images[page_index]
        separated_bbox = BboxSeparator().separate_bbox(bbox, page_image)
        prov_item.set_bbox(separated_bbox)
