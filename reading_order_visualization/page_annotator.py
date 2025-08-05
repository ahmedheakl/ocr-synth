from util.data_stores.docling_data_store import DoclingDataStore
from .bbox_annotator import BboxAnnotator
from .bbox_annotation_data import BboxAnnotationData
from .bbox_calculator import BboxCalculator
from .config.reading_order_annotation_config import ReadingOrderAnnotationConfig

class PageAnnotator:

    def __init__(self):
        self._bbox_annotator = BboxAnnotator()
        self._bbox_calculator = BboxCalculator()
        self._docling_data_store = DoclingDataStore()
        self._config = ReadingOrderAnnotationConfig()
        self._collected_warnings = {}

    def annotate_pages(self, pages, file_path):
        prev_bbox = self._gen_init_prev_bbox(pages)
        data = self._docling_data_store.get_main_text()

        current_page_index = 0
        for index, item in enumerate(data):
            if 'groups' in item['self_ref']:
                if 'inline' in item['label']:
                    item = self._docling_data_store.get_group_children(item['self_ref'])[0]
                elif 'list' in item['label']:
                    items = self._docling_data_store.get_group_children(item['self_ref'])
                    for item_list in items:
                        bbox_ann_data = self._get_bbox_annotation_data(pages, item_list)
                        for bbox_ann in bbox_ann_data:
                            if (current_page_index != bbox_ann.get_page_index()):
                                current_page_index = bbox_ann.get_page_index()
                                prev_bbox = self._gen_init_prev_bbox(pages)
                                self._bbox_annotator.create_bbox_flow_annotation(
                                    bbox_ann, index, prev_bbox)
                                prev_bbox = bbox_ann.get_bbox()
                            else:
                                self._bbox_annotator.create_bbox_flow_annotation(
                                    bbox_ann, index, prev_bbox)
                        try: prev_bbox = bbox_ann.get_bbox()
                        except: pass
                    continue
            bbox_ann_data = self._get_bbox_annotation_data(pages, item)
            for bbox_ann in bbox_ann_data:
                if (current_page_index != bbox_ann.get_page_index()):
                    current_page_index = bbox_ann.get_page_index()
                    prev_bbox = self._gen_init_prev_bbox(pages)
                    self._bbox_annotator.create_bbox_flow_annotation(
                        bbox_ann, index, prev_bbox)
                    prev_bbox = bbox_ann.get_bbox()
                else:
                    self._bbox_annotator.create_bbox_flow_annotation(
                        bbox_ann, index, prev_bbox)
            try: prev_bbox = bbox_ann.get_bbox()
            except: pass
        self._handle_collected_warnings(file_path)

    def _gen_init_prev_bbox(self, pages):
        horizontal_center = pages[0].width / 2
        return (horizontal_center, 0, horizontal_center, 0)

    def _get_bbox_annotation_data(self, pages, item) -> list:
        try:
            return self._collect_bbox_annotation_data(pages, item)
        except Exception as e:
            self._log_bbox_annotation_error(e)
            raise ValueError

    def _collect_bbox_annotation_data(self, pages, item) -> list:
        if (self._has_item_bbox_annotation(item)):
            return self._collect_text_annotation_data(pages, item)
        return self._collect_non_text_annotation_data(pages, item)

    def _has_item_bbox_annotation(self, json_item):
        return "prov" in json_item.keys()

    def _collect_text_annotation_data(self, pages, item) -> list:
        prov_data = item["prov"]
        return self._gen_bbox_annotations(prov_data, pages)
    
    def _collect_non_text_annotation_data(self, pages, item) -> list:
        category = self._get_item_category(item)
        index = self._extract_item_index(item)
        prov_data = self._ccs_data_store.get_data_item(category, index)["prov"]
        return self._gen_bbox_annotations(prov_data, pages)

    def _get_item_category(self, item):
        return item["type"] + "s"

    def _extract_item_index(self, data):
        ref = data["__ref"]
        id_ = int(ref.split("/")[-1])
        return id_

    def _gen_bbox_annotations(self, prov_data, pages) -> list:
        bbox_annotations = []
        for item in prov_data:
            page_index = item["page_no"] - 1
            page = pages[page_index]
            bbox_norm = self._get_normalized_bbox_coordinates(item, page_index)
            bbox_scaled = self._scale_bbox_values(bbox_norm, page)
            # bbox_scaled = [item["bbox"]['l'], item["bbox"]['t'], item["bbox"]['r'], item["bbox"]['b']]
            bbox_annotations.append(BboxAnnotationData(
                page, page_index, bbox_scaled))
        return bbox_annotations

    def _get_normalized_bbox_coordinates(self, item, page_index):
        h, w = self._docling_data_store.get_pages_pixel_dimension()
        normalized_bbox = [
            item["bbox"]['l'] / w,
            item["bbox"]['t'] / h,
            item["bbox"]['r'] / w,
            item["bbox"]['b'] / h
        ]
        return normalized_bbox
        # if (self._config.is_generated_latex_dataset()):
        #     return item["bbox"]
        # return self._model_to_annotation_bbox(item["bbox"], page_index)

    def _model_to_annotation_bbox(self, model_bbox, page_index):
        page_height = self._get_page_height(page_index)
        return (self._bbox_calculator
                .model_to_annotation_bbox_coordinates(model_bbox, page_height))

    def _scale_bbox_values(self, bbox_normalized: list[int], page):
        return [
            bbox_normalized[0] * page.width,
            bbox_normalized[1] * page.height,
            bbox_normalized[2] * page.width,
            bbox_normalized[3] * page.height
        ]

    def _get_page_height(self, page_index):
        try:
            return (self._ccs_data_store.
                get_page_dimensions_item(page_index)["height"])
        except:
            return self._handle_page_height_exception()

    def _handle_page_height_exception(self):
        message = ("Page dimensionality not available for each page. "
                    "Using page dimensionality of page one as a fallback.")
        if ("page-dim" not in self._collected_warnings):
            self._collected_warnings["page-dim"] = message
        return self._ccs_data_store.get_page_dimensions_item(0)["height"]

    def _log_bbox_annotation_error(self, exception):
        print(f"[ERROR] Bbox annotation data could not be collected:\n"
            f"{exception}")

    def _handle_collected_warnings(self, file_path):
        self._log_collected_warnings(file_path)
        self._clear_collected_warnings()

    def _log_collected_warnings(self, file_path):
        if (len(self._collected_warnings) > 0):
            print(f"[WARNING] Found warnings while parsing file: {file_path}")
            for message in self._collected_warnings.values():
                print(message)
            print("===========================================")

    def _clear_collected_warnings(self):
        self._collected_warnings = {}
