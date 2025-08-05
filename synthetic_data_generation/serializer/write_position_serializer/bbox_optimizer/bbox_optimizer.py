import numpy as np
from PIL import Image

from util.geometry_transformation.flipper import Flipper

class BboxOptimizer:

    def __init__(self):
        self._flipper = Flipper()
        self._max_iterations = 12
        self._whiteness_threshold = 255

    def optimize(
        self,
        bbox: list,
        image: Image,
        left=True,
        right=True,
        top=True,
        bottom=True,
        iterations=8
    ) -> list:
        if not (self.bbox_has_content(bbox, image)): return None
        iters = self._max_iterations if iterations > 8 else iterations
        oleft = self.optimize_left(bbox, image, iters) if left else bbox[0]
        oright = self.optimize_right(bbox, image, iters) if right else bbox[2]
        otop = self.optimize_top(bbox, image, iters) if top else bbox[1]
        obtm = self.optimize_bottom(bbox, image, iters) if bottom else bbox[3]
        return [oleft, otop, oright, obtm]
    
    def remove_big_bbox(self, bbox: list, image: Image):
        cropped_image = image.crop(bbox)
        numpy_image = np.array(cropped_image)
        white_pixel = np.array([255, 255, 255])
        first_text_in_bbox = 0
        for i in range(numpy_image.shape[0]):
            if any(numpy_image[i, :, 0] < white_pixel[0]) or any(numpy_image[i, :, 1] < white_pixel[1]) or any(numpy_image[i, :, 2] < white_pixel[2]):
                first_text_in_bbox = i
                break
        if (numpy_image.shape[0] - i < (numpy_image.shape[0] * 3)/ 4):
            return None
        else:
            return bbox
    
    def remove_big_bbox_by_ratio(self, bbox: list, image: Image):
        '''remove the bbox where the ratio of white pixel/ non white pixels
        is over a certain value
        The ratio threshold is a parametere defined empirically'''
        threshold = 0.78
        cropped_image = image.crop(bbox)
        numpy_image = np.array(cropped_image)
        white_pixel = np.array([255, 255, 255])
        print('print numpy image shape ', numpy_image.shape)
        non_white_rows = 0
        white_rows = 0
        for i in range(numpy_image.shape[0]):
            if any(numpy_image[i, :, 0] < white_pixel[0]) or any(numpy_image[i, :, 1] < white_pixel[1]) or any(numpy_image[i, :, 2] < white_pixel[2]):
                non_white_rows += 1
            else:
                white_rows += 1
        if white_rows == 0:
            return bbox
        if non_white_rows/(non_white_rows + white_rows) < threshold:
            return None
        else:
            return bbox
    
    def crop_section(self, bbox: list, image: Image):
        '''Remore the white lines that always remains on top
        and bottom of a section header'''
        cropped_image = image.crop(bbox)
        numpy_image = np.array(cropped_image)
        white_pixel = np.array([255, 255, 255])
        Found1 = False
        bottom = 0
        start = 0
        white_rows = 0
        non_white_rows = 0
        for i in range(numpy_image.shape[0]-1, -1, -1):
            if (any(numpy_image[i, :, 0] < white_pixel[0]) or any(numpy_image[i, :, 1] < white_pixel[1]) or any(numpy_image[i, :, 2] < white_pixel[2])) and not Found1:
                Found1 = True
                bottom = i
                # print(f'bottom {bottom}')
            elif (any(numpy_image[i, :, 0] < white_pixel[0]) or any(numpy_image[i, :, 1] < white_pixel[1]) or any(numpy_image[i, :, 2] < white_pixel[2])) and Found1:
                non_white_rows += 1
                start = i
                white_rows = 0
            elif white_rows > 10:
                #if 10 consequently white rows, stop
                break
            elif Found1:
                white_rows += 1
            else:
                pass
                
        # print(f'difference {bottom - start}')
        # print(f"non white rows {non_white_rows}")
        # if (bottom - start) < numpy_image.shape[0]*0.2:
        #     return None
        # print('new box')
        # print(f'start {start}')
        # print(f'bottom {bottom}')
        bbox[3] = bbox[1] + bottom
        bbox[1] = bbox[1] + start
        return bbox
        
    def bbox_has_content(self, bbox, image):
        return self._image_has_content(image.crop(bbox))

    def optimize_left(self, bbox: list, image: Image, iterations=8) -> int:
        return self._optimize_left(image.crop(bbox), bbox[0], iterations)

    def optimize_right(self, bbox, image, iterations=8) -> int:
        bbox_crop = image.crop(bbox).transpose(Image.FLIP_LEFT_RIGHT)
        oleft_crop = self._optimize_left(bbox_crop, 0, iterations)
        return bbox[0] + self._oleft_to_oright(oleft_crop, bbox_crop)

    def _oleft_to_oright(self, oleft, image) -> int:
        return self._flipper.flip(oleft, 0, image.width-1)

    def optimize_top(self, bbox: list, image: Image, iterations=8) -> int:
        bbox_crop, left = self._top_to_left_state(bbox, image)
        return self._optimize_left(bbox_crop, left, iterations)
    
    def _top_to_left_state(self, bbox, image):
        bbox_crop = image.crop(bbox).rotate(90, Image.NEAREST, expand=1)
        left = bbox[1]
        return bbox_crop, left

    def optimize_bottom(self, bbox: list, image: Image, iterations=8) -> int:
        bbox_crop, left = self._bottom_to_left_state(bbox, image)
        oleft = self._optimize_left(bbox_crop, left, iterations)
        return image.height - oleft

    def _bottom_to_left_state(self, bbox, image):
        bbox_crop = image.crop(bbox).rotate(-90, Image.NEAREST, expand=1)
        left = image.height - bbox[3]
        return bbox_crop, left

    def _optimize_left(self, image, left, iterations) -> int:
        if (iterations == 0): return left
        left_width = image.width // 2
        if (left_width < 2): return left
        left_crop = image.crop([0, 0, left_width-1, image.height])
        if (self._image_has_content(left_crop)):
            return self._optimize_left(left_crop, left, iterations-1)
        right_crop = image.crop([left_width, 0, image.width-1, image.height])
        return self._optimize_left(right_crop, left+left_width, iterations-1)

    def _image_has_content(self, image):
        px_mean = np.mean(np.array(image))
        return px_mean < self._whiteness_threshold
