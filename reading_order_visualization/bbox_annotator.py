from PIL import ImageDraw, ImageFont

from reading_order_visualization.bbox_calculator import BboxCalculator
from reading_order_visualization.bbox_connection_drawer import BboxConnectionDrawer
from reading_order_visualization.draw_color import DrawColor

class BboxAnnotator:

    def __init__(self):
        self._bbox_calculator = BboxCalculator()
        self._bbox_connection_drawer = BboxConnectionDrawer()
        self._draw_color = DrawColor()
        self._font = ImageFont.load_default() # dpi = 120
        # self._font = ImageFont.truetype(
        #     "/System/Library/Fonts/Supplemental/Arial.ttf", 120) # dpi = 960
        self._cnt = 0
        self._dark_blue = (0, 0, 204)
        self._light_blue = (77, 184, 255)

    def create_bbox_flow_annotation(
            self, bbox_annotation_data, index, prev_bbox):
        self._draw_bbox(bbox_annotation_data)
        self._write_bbox_text(bbox_annotation_data, index)
        self._draw_connection_line(bbox_annotation_data, prev_bbox)
        self._cnt += 1

    def _draw_bbox(self, bbox_annotation_data):
        draw_image = ImageDraw.Draw(bbox_annotation_data.get_page())
        width = 1 # dpi = 120
        # width = 12 # dpi = 960
        draw_image.rectangle(bbox_annotation_data.get_bbox(),
            outline=self._draw_color.get_color(self._cnt), width=width)

    def _write_bbox_text(self, bbox_annotation_data, bbox_index):
        pnt = self._bbox_calculator.compute_bbox_top_center_pnt(
            bbox_annotation_data.get_bbox())
        draw = ImageDraw.Draw(bbox_annotation_data.get_page())
        # dpi = 120
        draw.text((pnt[0]+6, pnt[1]-12),
            f"{bbox_index}, {bbox_annotation_data.get_page_num()}",
            font=self._font, fill=self._draw_color.get_color(self._cnt))
        # dpi = 960
        # draw.text((pnt[0] - 160, pnt[1] - 160),
        #     f"{bbox_index}",
        #     font=self._font, fill=self._draw_color.get_color(self._cnt))

    def _draw_connection_line(self, bbox_annotation_data, prev_bbox):
        self._bbox_connection_drawer.draw_connection(
            bbox_annotation_data.get_page(),
            prev_bbox, bbox_annotation_data.get_bbox())
