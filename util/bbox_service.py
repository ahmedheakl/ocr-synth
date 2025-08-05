"""
Entails convenience functions for divers operations with bboxes.
"""

def is_point_in_bbox(left: int, top: int, bbox: list[int]):
    return (((left > bbox[0]) and (left < bbox[2])) and
        ((top > bbox[1]) and (top < bbox[3])))
