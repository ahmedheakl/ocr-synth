from synthetic_data_generation.serializer.write_position_serializer.data_structures.bbox import Bbox

class ContentPosition:

    def __init__(
        self,
        x_pos_start: int,
        y_pos_start: int,
        x_pos_end: int,
        y_pos_end: int
    ):
        # Provide all input arg values in unit px!
        self._x_pos_start = x_pos_start
        self._y_pos_start = y_pos_start
        self._x_pos_end = x_pos_end
        self._y_pos_end = y_pos_end

    def get_x_pos_start(self):
        return self._x_pos_start

    def get_y_pos_start(self):
        return self._y_pos_start

    def get_x_pos_end(self):
        return self._x_pos_end

    def get_y_pos_end(self):
        return self._y_pos_end

    def get_content_width(self):
        return abs(self._x_pos_end - self._x_pos_start)
    
    def get_content_height(self):
        return abs(self._y_pos_end - self._y_pos_start)

    def set_x_pos_start(self, value: int):
        self._x_pos_start = value

    def set_y_pos_start(self, value: int):
        self._y_pos_start = value

    def set_x_pos_end(self, value: int):
        self._x_pos_end = value

    def set_y_pos_end(self, value: int):
        self._y_pos_end = value

    def is_located_in_bbox(self, bbox: Bbox):
        return not ((self._x_pos_end < bbox.get_left()) or
            (self._x_pos_start > bbox.get_right()))

    def to_bbox_coordinates(self):
        return [
            self._x_pos_start,
            self._y_pos_start,
            self._x_pos_end,
            self._y_pos_end
        ]

    def __str__(self):
        return (
            "Content position:\n"
            f"x_start = {self._x_pos_start} px\n"
            f"y_start = {self._y_pos_start} px\n"
            f"x_end   = {self._x_pos_end} px\n"
            f"y_end   = {self._y_pos_end} px\n"
            "=========================================="
        )
