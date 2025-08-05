class BboxAnnotationData:

    def __init__(self, page, page_index, bbox):
        self._page = page
        self._page_index = page_index
        self._bbox = bbox
    
    def get_page(self):
        return self._page
    
    def get_page_index(self):
        return self._page_index

    def get_page_num(self):
        return self._page_index + 1

    def get_bbox(self):
        return self._bbox
