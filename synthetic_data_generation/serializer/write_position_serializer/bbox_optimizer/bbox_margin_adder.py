from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox

class BboxMarginAdder:

    def __init__(self):
        # Values are in unit px.
        self._padding_left = 3
        self._padding_right = 3
        self._padding_top = 3
        self._padding_bottom = 2

    def add_margin_to_bbox_list(self, bbox: list):
        bbox[0] -= self._padding_left
        bbox[1] -= self._padding_top
        bbox[2] += self._padding_right
        bbox[3] += self._padding_bottom

    def add_margin_to_bbox_item(self, bbox: Bbox):
        bbox.set_left(bbox.get_left() - self._padding_left)
        bbox.set_right(bbox.get_right() + self._padding_right)
        bbox.set_top(bbox.get_top() - self._padding_top)
        bbox.set_bottom(bbox.get_bottom() + self._padding_bottom)
