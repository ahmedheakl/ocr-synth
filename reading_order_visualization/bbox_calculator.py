class BboxCalculator:

    def compute_bbox_top_center_pnt(self, bbox_coordinates):
        x0, y0, x1, _ = bbox_coordinates
        x = (x1 - x0) / 2 + x0
        return (x, y0)

    def compute_bbox_bottom_center_pnt(self, bbox_coordinates):
        x0, _, x1, y1 = bbox_coordinates
        x = (x1 - x0) / 2 + x0
        return (x, y1)

    def model_to_annotation_bbox_coordinates(self, model_coordinates, page_height):
        draw_coordinates = [
            model_coordinates[0],
            page_height - model_coordinates[3],
            model_coordinates[2],
            page_height - model_coordinates[1]
        ]
        return draw_coordinates
