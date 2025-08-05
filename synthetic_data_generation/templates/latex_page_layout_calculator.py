from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class LatexPageLayoutCalculator:

    def __init__(self):
        self._one_inch_pt = 72

    def calc_even_page_text_x_origin(self, layout_style: dict) -> float:
        # Using the geometry package, even and odd pages have the same layout.
        return self.calc_odd_page_text_x_origin(layout_style)

    def calc_odd_page_text_x_origin(self, layout_style: dict) -> float:
        return (self._one_inch_pt + layout_style[TemplateKeys.H_OFFSET] +
            layout_style[TemplateKeys.ODD_SIDE_MARGIN])

    def calc_text_y_origin(self, layout_style: dict) -> float:
        return (self._one_inch_pt + layout_style[TemplateKeys.V_OFFSET] +
            layout_style[TemplateKeys.TOP_MARGIN] +
            layout_style[TemplateKeys.HEAD_HEIGHT] +
            layout_style[TemplateKeys.HEAD_SEP])

    def calc_text_y_end(self, layout_style: dict) -> float:
        return (self.calc_text_y_origin(layout_style) +
            layout_style[TemplateKeys.TEXT_HEIGHT])

    def calc_head_top(self, layout_style: dict) -> float:
        return (self._one_inch_pt + layout_style[TemplateKeys.V_OFFSET] +
            layout_style[TemplateKeys.TOP_MARGIN])

    def calc_foot_top(self, layout_style: dict) -> float:
        return (self.calc_text_y_end(layout_style) +
            layout_style[TemplateKeys.FOOT_SKIP] -
            layout_style[TemplateKeys.FOOT_HEIGHT])
