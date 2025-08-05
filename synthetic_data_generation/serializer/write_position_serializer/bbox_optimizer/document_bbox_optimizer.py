from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_data import GroundTruthData
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_item import GroundTruthItem
from synthetic_data_generation.serializer.write_position_serializer.bbox_optimizer.bbox_margin_adder import BboxMarginAdder
from synthetic_data_generation.serializer.write_position_serializer.bbox_optimizer.bbox_optimizer import BboxOptimizer
from util.latex_item_type_names import LatexItemTypeNames
from .document_items_bbox_separator import DocumentItemsBboxSeparator
from .document_items_empty_bbox_remover import DocumentItemsEmptyBboxRemover
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.util.unit_converter import UnitConverter

class DocumentBboxOptimizer:

    def __init__(self, gt_data: GroundTruthData, page_images: list):
        self._gt_data = gt_data
        self._page_images = page_images
        self._bbox_margin_adder = BboxMarginAdder()
        self._bbox_optimizer = BboxOptimizer()
        self._bbox_separator = DocumentItemsBboxSeparator()
        self._layout_settings = Template().get_layout_settings()

    def optimize_bboxes(self, pos_stores):
        self._remove_empty_bboxes(pos_stores)
        self._optimize_bboxes()
        # self._optimize_sections()
        # self._remove_too_big_bboxes()

    def _optimize_sections(self):
        #custom optimization for the section text dimension
        #doesn't take into account multiplem lines (BAD)
        for item in self._gt_data.get_data():
            if 'section' in item.to_reading_order_format()[0]['label']:
                prov_items = item.get_prov().get_items()
                prov =  item.get_prov()
                for i, prov_item in enumerate(prov_items):
                    bbox = prov_item.get_bbox()
                    section_height_sp = self._layout_settings.get_section_size_sp()
                    section_top = bbox[3] - UnitConverter().sp_to_px(section_height_sp)
                    if section_top > bbox[1]:
                        bbox[1] = section_top
                        prov_item.set_bbox(bbox)

    def _remove_too_big_bboxes(self):
        for item in self._gt_data.get_data():
            if 'table' in item.to_reading_order_format()[0]['self_ref']:
                continue
            if 'pictures' in item.to_reading_order_format()[0]['self_ref']:
                continue
            prov_items = item.get_prov().get_items()
            prov =  item.get_prov()
            deleted_items = 0
            for i, prov_item in enumerate(prov_items):
                bbox = prov_item.get_bbox()
                page_index = prov_item.get_page_num() - 1
                page_image = self._page_images[page_index]
                obbox = self._bbox_optimizer.remove_big_bbox(bbox, page_image)
                if obbox is None and prov.get_num_items()>0:
                    prov.pop(i - deleted_items)
                    deleted_items += 1
                obbox = self._bbox_optimizer.remove_big_bbox_by_ratio(bbox, page_image)
                if obbox is None and prov.get_num_items()> 0:
                    prov.pop(i - deleted_items)
                    deleted_items += 1

    def _remove_empty_bboxes(self, pos_stores):
        DocumentItemsEmptyBboxRemover().remove_empty_bboxes(
            self._gt_data, self._page_images, pos_stores)

    def _optimize_bboxes(self):
        for item in self._gt_data.get_data():
            # if 'table' in item.to_reading_order_format()[0]['self_ref']:
            #     #just for debug
            #     print('optimizing a table')
            #     print(f'item to optimize boxes {item.to_reading_order_format()[0]}')
            #if section, there's always the problem of the white space before due to
            #the fact that the position is latex is always related to the previuous text baseline
            if 'section' in item.to_reading_order_format()[0]['label']:
                prov_items = item.get_prov().get_items()
                prov =  item.get_prov()
                for i, prov_item in enumerate(prov_items):
                    bbox = prov_item.get_bbox()
                    page_index = prov_item.get_page_num() - 1
                    page_image = self._page_images[page_index]
                    obbox = self._bbox_optimizer.crop_section(bbox,page_image)
                    if obbox is not None:
                        prov_item.set_bbox(obbox)
            if (self._are_item_bboxes_to_optimize(item)):
                self._separate_item_bboxes(item)
                self._optimize_item_bboxes(item)
            self._optimize_line_nums_bboxes(item)
            # self._add_margins_to_bboxes(item)

    def _are_item_bboxes_to_optimize(self, item: GroundTruthItem):
        return (
            item.is_list_item() or
            item.is_spread_across_multiple_latex_pages() or
            not self._is_item_type_paragraph(item) or
            not self._is_prev_item_type_paragraph(item))

    def _is_item_type_paragraph(self, item: GroundTruthItem):
        return (item.get_type() == LatexItemTypeNames.PARAGRAPH)

    def _is_prev_item_type_paragraph(self, item: GroundTruthItem):
        item_index = item.get_index()
        prev_item_index = item_index - 1
        prev_item = self._gt_data.get_item(prev_item_index)
        if (prev_item is None): return False
        return (prev_item.get_type() == LatexItemTypeNames.PARAGRAPH)

    def _separate_item_bboxes(self, item: GroundTruthItem):
        self._bbox_separator.separate_item_bboxes_from_other_items(
            item, self._gt_data, self._page_images)

    def _optimize_item_bboxes(self, item: GroundTruthItem):
        prov_items = item.get_prov().get_items()
        for prov_item in prov_items:
            self._optimize_item_bbox(prov_item)

    def _optimize_item_bbox(self, prov_item: ProvItem):
        bbox = prov_item.get_bbox()
        page_index = prov_item.get_page_num() - 1
        page_image = self._page_images[page_index]
        obbox = self._bbox_optimizer.optimize(bbox, page_image, iterations=8)
        if (obbox is not None): prov_item.set_bbox(obbox)

    def _optimize_line_nums_bboxes(self, item: GroundTruthItem):
        line_nums = item.get_line_nums()
        prov = line_nums.get_prov()
        for prov_item in prov.get_items():
            self._optimize_item_bbox(prov_item)

    def _add_margins_to_bboxes(self, item: GroundTruthItem):
        main_text_prov = item.get_prov()
        self._add_margins_to_prov_items(main_text_prov.get_items())
        line_nums_prov = item.get_line_nums().get_prov()
        self._add_margins_to_prov_items(line_nums_prov.get_items())

    def _add_margins_to_prov_items(self, prov_items: list[ProvItem]):
        for prov_item in prov_items:
            bbox = prov_item.get_bbox()
            self._bbox_margin_adder.add_margin_to_bbox_list(bbox)
