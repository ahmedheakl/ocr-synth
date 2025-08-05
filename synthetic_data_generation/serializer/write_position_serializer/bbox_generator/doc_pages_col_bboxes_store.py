from copy import deepcopy

from synthetic_data_generation.templates.template import Template
from .page_bbox_bounds_scanner import PageBboxBoundsScanner

class DocPagesColBboxesStore:
    """
    Stores the bboxes of the content columns of every page of the currently
    processed document. Content column bboxes can vary in size. If e.g. figures
    or tables span the whole page width at the top or bottom of the page,
    the regular content col bboxes must be adjusted, i.e. they cannot simply
    go from the page top to the page bottom. These adjusted bboxes are stored
    in this singleton class after they are computed for a page such that they
    can be quickly retrieved when needed. This avoids unnecessary recomputing
    which is costly as it needs to load the page image and process it.
    """

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(DocPagesColBboxesStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._doc_pages_col_bboxes = {}

    def clear(self):
        self._doc_pages_col_bboxes = {}

    def get_or_create_page_col_bboxes(self, page_num: int) -> list:
        if (page_num in self._doc_pages_col_bboxes):
            return deepcopy(self._doc_pages_col_bboxes[page_num])
        _page_col_bboxes = self._gen_page_col_bboxes(page_num)
        self._doc_pages_col_bboxes[page_num] = _page_col_bboxes
        return deepcopy(self._doc_pages_col_bboxes[page_num])

    def _gen_page_col_bboxes(self, page_num: int) -> list:
        layout_settings = Template().get_layout_settings()
        page_col_bboxes = layout_settings.get_page_cols_bboxes(page_num)
        self._set_page_num_of_bboxes(page_num, page_col_bboxes)
        (top, bottom) = self._find_vertical_limits_of_page_cols(page_num)
        self._apply_vertical_limits_on_latex_page_cols(page_col_bboxes, top, bottom)
        return page_col_bboxes

    def _set_page_num_of_bboxes(self, page_num: int, page_col_bboxes: list):
        for page_col_bbox in page_col_bboxes:
            page_col_bbox.set_page_num(page_num)

    def _find_vertical_limits_of_page_cols(
        self, page_num: int
    ) -> tuple[int, int]:
        scanner = PageBboxBoundsScanner()
        (top, bottom) = scanner.scan_page_for_vertical_bbox_bounds(page_num)
        return (top, bottom)

    def _apply_vertical_limits_on_latex_page_cols(
        self, page_col_bboxes: list, top: int, bottom: int
    ):
        for page_col_bbox in page_col_bboxes:
            page_col_bbox.set_top(top)
            page_col_bbox.set_bottom(bottom)
