class Bbox:

    def __init__(self, coordinates, page_num=None, span=[]):
        self._coordinates = coordinates
        self._page_num = page_num
        self._span = span

    def get_coordinates(self):
        return self._coordinates[:]

    def get_page_num(self) -> int:
        return self._page_num

    def get_left(self):
        return self._coordinates[0]

    def get_right(self):
        return self._coordinates[2]

    def get_top(self):
        return self._coordinates[1]

    def get_bottom(self):
        return self._coordinates[3]

    def get_width(self):
        return self.get_right() - self.get_left()

    def get_height(self):
        return self.get_bottom() - self.get_top()

    def set_left(self, value: int):
        self._coordinates[0] = value

    def set_right(self, value: int):
        self._coordinates[2] = value

    def set_top(self, value: int):
        self._coordinates[1] = value

    def set_bottom(self, value: int):
        self._coordinates[3] = value

    def set_page_num(self, page_num: int):
        self._page_num = page_num

    def includes_x_pos(self, x_pos: int) -> bool:
        return ((x_pos > self.get_left()) and
            (x_pos < self.get_right()))

    def to_prov_item_dict(self) -> dict:
        return {
            "bbox": self._coordinates,
            "page_no": self._page_num,
            "charspan": self._span
        }

    def __str__(self) -> str:
        return (
            f"Page num = {self._page_num}, "
            f"{self.get_coordinates()}"
        )
