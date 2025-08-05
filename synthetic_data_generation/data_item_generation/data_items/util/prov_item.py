from synthetic_data_generation.templates.template import Template

class ProvItem:

    def __init__(self, prov: dict):
        self._bbox = prov["bbox"]
        self._page_num = prov["page_no"]
        self._span = prov["charspan"]
        if len(self._span) == 0:
            self._span = (0,0) 

    def get_bbox(self) -> list[int]:
        return self._bbox

    def get_bbox_normalized(self) -> list[float]:
        return self._normalize_bbox()

    def set_bbox(self, bbox: list):
        self._bbox = bbox

    def get_page_num(self) -> int:
        return self._page_num

    def get_page_col_bbox_index(self) -> int:
        layout_settings = Template().get_layout_settings()
        page_cols_bboxes = layout_settings.get_page_cols_bboxes(self._page_num)
        for index, page_cols_bbox in enumerate(page_cols_bboxes):
            if (self._bbox[0] < page_cols_bbox.get_right()):
                return index

    def get_span(self):
        return self._span

    # def to_dict(self) -> dict:
    #     return {
    #         "bbox": self._normalize_bbox(),
    #         "page_no": self._page_num,
    #         "char_span": self._span
    #     }

    def to_dict(self) -> dict:
        return {
            "bbox": self._docling_bbox(),
            "page_no": self._page_num,
            "charspan": self._span,
            "charspan": self._span
        }

    def _normalize_bbox(self):
        layout_settings = Template().get_layout_settings()
        page_width = layout_settings.get_page_width_px()
        page_height = layout_settings.get_page_height_px()
        # print('page dimensions in px')
        # print(page_width)
        # print(page_height)
        normalized_bbox = [
            self._bbox[0] / page_width,
            self._bbox[1] / page_height,
            self._bbox[2] / page_width,
            self._bbox[3] / page_height
        ]
        return normalized_bbox

    def _docling_bbox(self) -> dict:
        '''In the generated DoclingDocuments, we want the actual dimension in pixel
        Not the normalized dimension based on the image.'''
        docling_dict = {}
        docling_dict['l'] = self._bbox[0]
        docling_dict['t'] = self._bbox[1]
        docling_dict['r'] = self._bbox[2]
        docling_dict['b'] = self._bbox[3]
        docling_dict['coord_origin'] = "TOPLEFT"
        return docling_dict