def ccs_to_pil_bbox(ccs_bbox: list, page_height):
    return [
        ccs_bbox[0],
        page_height - ccs_bbox[3],
        ccs_bbox[2],
        page_height - ccs_bbox[1]
    ]

def pil_to_ccs_bbox(pil_bbox: list, page_height):
    return [
        pil_bbox[0],
        page_height - pil_bbox[3],
        pil_bbox[2],
        page_height - pil_bbox[1]
    ]
