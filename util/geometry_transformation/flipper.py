from PIL import Image

class Flipper:

    def flip_image_horizontally(self, image):
        return image.transpose(Image.FLIP_LEFT_RIGHT)

    def flip_image_vertically(self, image):
        return image.transpose(Image.FLIP_TOP_BOTTOM)

    def flip_bbox_horizontally(self, bbox, image):
        left = self.flip_to_left(bbox[2], 0, image.width-1)
        right = self.flip_to_right(bbox[0], 0, image.width-1)
        return [left, bbox[1], right, bbox[3]]

    def flip(self, value, left_edge, right_edge):
        if (value > self.compute_center_coordinate(left_edge, right_edge)):
            return self.flip_to_left(value, left_edge, right_edge)
        return self.flip_to_right(value, left_edge, right_edge)

    def flip_to_left(self, right, left_edge, right_edge):
        if (right < self.compute_center_coordinate(left_edge, right_edge)):
            return right
        d = self.compute_distance_to_center(right, left_edge, right_edge)
        if (self._is_even_length(left_edge, right_edge)):
            return right - (2 * d) + 1
        return right - (2 * d)

    def flip_to_right(self, left, left_edge, right_edge):
        if (left > self.compute_center_coordinate(left_edge, right_edge)):
            return left
        d = self.compute_distance_to_center(left, left_edge, right_edge)
        if (self._is_even_length(left_edge, right_edge)):
            return left + 2*d + 1
        return left + 2*d

    def compute_distance_to_center(self, value, edge1, edge2):
        center = self.compute_center_coordinate(edge1, edge2)
        return abs(value - center)

    def compute_center_coordinate(self, v1, v2):
        return abs(v2 - v1) // 2

    def _is_even_length(self, v1, v2):
        return abs(v1 - v2) % 2
