from synthetic_data_generation.data_item_generation.data_items.util.prov import Prov
from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.serializer.write_position_serializer.bbox_optimizer.bbox_optimizer import BboxOptimizer
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_data import GroundTruthData
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_item import GroundTruthItem
from synthetic_data_generation.templates.template import Template

class DocumentItemsEmptyBboxRemover:

    def remove_empty_bboxes(self, gt_data: GroundTruthData, page_images: list, pos_stores):
        for item in gt_data.get_data():
            # if 'table' in item.to_reading_order_format()[0]['self_ref']:
            #     print('checking if empty boxes for table')
            #     continue
            self._remove_empty_main_text_bboxes(item, page_images, pos_stores)
            self._remove_empty_line_num_bboxes(item, page_images, pos_stores)

    def _remove_empty_main_text_bboxes(
        self, item: GroundTruthItem, page_images: list, pos_stores
    ):
        prov = item.get_prov()
        index = item.get_index()
        pos_object = pos_stores.get_or_none_item(index)
        indexes = self._find_indexes_of_empty_bboxes(prov, page_images, pos_object)
        self._remove_empty_bboxes_of_indexes(prov, indexes)

    def _remove_empty_line_num_bboxes(self, item: GroundTruthItem, page_images: list, pos_stores):
        line_nums = item.get_line_nums()
        prov = line_nums.get_prov()
        index = item.get_index()
        pos_object = pos_stores.get_or_none_item(index)
        indexes = self._find_indexes_of_empty_bboxes(prov, page_images, pos_object, True)
        self._remove_empty_bboxes_of_indexes(prov, indexes)

    def _find_indexes_of_empty_bboxes(
        self, prov: Prov, page_images: list, pos_object, is_line_num: bool=False
    ) -> list[int]:
        empty_bbox_indexes = []
        print(pos_object)
        if pos_object:
            y = pos_object.get_first_word_y()
            layout = Template().get_layout_settings()
            page_size = layout.get_page_height_px()
        for index, prov_item in enumerate(prov.get_items()):
            if index == 0 and pos_object and (abs(prov_item.get_bbox()[1] - y) > page_size/2 ):
                empty_bbox_indexes.append(index)
                continue
            if (self._is_bbox_empty(prov_item, page_images, is_line_num)):
                empty_bbox_indexes.append(index)
        return empty_bbox_indexes

    def _is_bbox_empty(
        self, prov_item: ProvItem, page_images: list, is_line_num: bool
    ) -> bool:
        page_index = prov_item.get_page_num() - 1
        image = page_images[page_index]
        bbox = prov_item.get_bbox()
        if (is_line_num):
            return not BboxOptimizer().bbox_has_content(bbox, image)
        return (not self._is_bbox_high_enough(bbox) or
                not BboxOptimizer().bbox_has_content(bbox, image))

    def _is_bbox_high_enough(self, bbox: list) -> bool:
        bbox_height = bbox[3] - bbox[1]
        margin_value = 5 # [px] Optimized value via trial and error.
        layout_settings = Template().get_layout_settings()
        text_size = layout_settings.get_font_size_px()
        min_height = text_size - margin_value
        return bbox_height > min_height

    def _remove_empty_bboxes_of_indexes(self, prov: Prov, indexes: list):
        indexes.sort(reverse=True)
        for index in indexes:
            prov.pop(index)
