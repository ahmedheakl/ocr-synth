import numpy as np
from PIL import Image

class ImageStripe:

    _white_pixel_value = 255

    def __init__(self, width):
        self._left = 0
        self._right = self._left + width
        self._height = 8 # [px] Optimized value via trial and error.
        self._top = 0
        self._bottom = self._top + self._height

    def get_top(self):
        return self._top
    
    def get_bottom(self):
        return self._bottom

    def is_all_white(self, image: Image):
        stripe_bbox = self._to_bbox()
        stripe_crop = image.crop(stripe_bbox)
        px_mean = np.mean(np.array(stripe_crop))
        return px_mean == ImageStripe._white_pixel_value

    def shift_to_init_position(self):
        """
        In the majority of cases, the bbox overlaps with another object by only
        very few pixels. To skip this overlap, this function shifts the strip
        by a small number of pixels towards the image bottom.
        """
        shift = 2 # [px]
        self._top = self._top + shift
        self._bottom = self._bottom + shift

    def shift_towards_bottom_by_one_height(self):
        self._top = self._bottom
        self._bottom = self._top + self._height

    def sticks_out_of_item_bbox(self, item_bbox: list):
        return (item_bbox[3] < (item_bbox[1] + self._bottom))

    def _to_bbox(self):
        return [self._left, self._top, self._right, self._bottom]

class BboxSeparator:

    _white_pixel_value = 255

    def separate_bbox(self, item_bbox: list, page_image: Image):
        item_image = page_image.crop(item_bbox)
        stripe = ImageStripe(item_image.width)
        self._shift_stripe_down_until_it_is_all_white(stripe, item_image,
                                                      item_bbox)
        if (stripe.sticks_out_of_item_bbox(item_bbox)):
            return item_bbox
        separated_bbox = self._gen_separated_bbox(item_bbox, stripe)
        if (self._has_separate_bbox_image_content(separated_bbox, page_image)):
            return separated_bbox
        return item_bbox

    def _shift_stripe_down_until_it_is_all_white(
            self, stripe: ImageStripe, item_image: Image, item_bbox: list):
        stripe.shift_to_init_position()
        while (not (stripe.is_all_white(item_image)) and
            not (stripe.sticks_out_of_item_bbox(item_bbox))):
            stripe.shift_towards_bottom_by_one_height()

    def _has_separate_bbox_image_content(
            self, separated_bbox: list, page_image: Image):
        image_below_stripe = page_image.crop(separated_bbox)
        px_mean = np.mean(np.array(image_below_stripe))
        return (px_mean < BboxSeparator._white_pixel_value)

    def _gen_separated_bbox(self, item_bbox: list, stripe: ImageStripe):
        return [
            item_bbox[0],
            item_bbox[1] + stripe.get_top(),
            item_bbox[2],
            item_bbox[3]
        ]
