from PIL import ImageDraw

from reading_order_visualization.bbox_calculator import BboxCalculator
from reading_order_visualization.draw_color import DrawColor

class BboxConnectionDrawer:

    def __init__(self):
        self._bbox_calculator = BboxCalculator()
        self._draw_color = DrawColor()
        self._cnt = 0

    def draw_connection(self, image, bbox0, bbox1):
        draw = ImageDraw.Draw(image)
        pnt0 = self._bbox_calculator.compute_bbox_bottom_center_pnt(bbox0)
        pnt1 = self._bbox_calculator.compute_bbox_top_center_pnt(bbox1)
        self._draw_line(draw, pnt0, pnt1)
        self._draw_marker(draw, pnt1)
        self._cnt += 1

    def _draw_line(self, draw, pnt0, pnt1):
        width = 1 # dpi = 120
        # width = 6 # dpi = 960
        draw.line((pnt0, pnt1), fill=self._draw_color.get_color(self._cnt),
                  width=width)

    def _draw_marker(self, draw, pnt):
        draw.ellipse((pnt[0]-3, pnt[1] - 3, pnt[0]+3, pnt[1] + 3),
                     fill=self._draw_color.get_color(self._cnt))
