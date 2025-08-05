from .unit_converter import UnitConverter

class LatexPageSettings:

    def __init__(self):
        # All units are in pt.
        self._one_inch = 72

        self._page_width = 614.295
        self._page_height = 794.97

        self._text_width = 430.00462
        self._text_height = 556.47656
        self._text_parindent = 15

        self._h_offset = 0
        self._odd_side_margin = 19.8752
        self._odd_page_text_x_origin = (self._one_inch + self._h_offset +
                                        self._odd_side_margin)
        self._even_page_text_x_origin = self._odd_page_text_x_origin

        self._v_offset = 0
        self._top_margin = -13.87262
        self._head_height = 12
        self._head_sep = 25
        self._head_top = self._one_inch + self._v_offset + self._top_margin

        self._text_y_origin = (self._one_inch + self._v_offset +
                               self._top_margin + self._head_height +
                               self._head_sep)
        self._text_y_end = self._text_y_origin + self._text_height

        self._foot_skip = 30
        self._foot_height = 9
        self._foot_top = self._text_y_end + self._foot_skip - self._foot_height

        self._baseline_skip = 12

        self._unit_converter = UnitConverter()

    def get_page_size_px(self):
        return (self.get_page_width_px(), self.get_page_height_px())

    def get_page_width_px(self):
        return self._unit_converter.pt_to_px(self._page_width)
    
    def get_page_height_px(self):
        return self._unit_converter.pt_to_px(self._page_height)


    def get_baseline_skip_px(self):
        return self._unit_converter.pt_to_px(self._baseline_skip)


    def get_head_top_px(self):
        return self._unit_converter.pt_to_px(self._head_top)

    def get_foot_top_px(self):
        return self._unit_converter.pt_to_px(self._foot_top)


    def get_text_width_pt(self):
        return self._text_width

    def get_text_width_px(self):
        return self._unit_converter.pt_to_px(self._text_width)

    def get_text_height_px(self):
        return self._unit_converter.pt_to_px(self._text_height)


    def get_page_text_x_origin_pt(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_origin_pt()
        return self.get_odd_page_text_x_origin_pt()

    def get_page_text_x_origin_px(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_origin_px()
        return self.get_odd_page_text_x_origin_px()

    def get_page_text_x_origin_sp(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_origin_sp()
        return self.get_odd_page_text_x_origin_sp()

    def get_page_text_x_end_pt(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_end_pt()
        return self.get_odd_page_text_x_end_pt()

    def get_page_text_x_end_px(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_end_px()
        return self.get_odd_page_text_x_end_px()

    def get_page_text_x_end_sp(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_end_sp()
        return self.get_odd_page_text_x_end_sp()


    def get_even_page_text_x_origin_pt(self):
        return self._even_page_text_x_origin

    def get_even_page_text_x_origin_px(self):
        return self._unit_converter.pt_to_px(self._even_page_text_x_origin)

    def get_even_page_text_x_origin_sp(self):
        return self._unit_converter.pt_to_sp(self._even_page_text_x_origin)

    def get_even_page_text_x_end_pt(self):
        return self._even_page_text_x_origin + self._text_width

    def get_even_page_text_x_end_px(self):
        return self._unit_converter.pt_to_px(
            self.get_even_page_text_x_end_pt())

    def get_even_page_text_x_end_sp(self):
        return self._unit_converter.pt_to_sp(
            self.get_even_page_text_x_end_pt())

    def get_odd_page_text_x_origin_pt(self):
        return self._odd_page_text_x_origin

    def get_odd_page_text_x_origin_px(self):
        return self._unit_converter.pt_to_px(self._odd_page_text_x_origin)

    def get_odd_page_text_x_origin_sp(self):
        return self._unit_converter.pt_to_sp(self._odd_page_text_x_origin)

    def get_odd_page_text_x_end_pt(self):
        return self._odd_page_text_x_origin + self._text_width

    def get_odd_page_text_x_end_px(self):
        return self._unit_converter.pt_to_px(self.get_odd_page_text_x_end_pt())

    def get_odd_page_text_x_end_sp(self):
        return self._unit_converter.pt_to_sp(self.get_odd_page_text_x_end_pt())


    def get_text_y_origin_pt(self):
        return self._text_y_origin

    def get_text_y_origin_px(self):
        return self._unit_converter.pt_to_px(self._text_y_origin)

    def get_text_y_origin_sp(self):
        return self._unit_converter.pt_to_sp(self._text_y_origin)

    def get_text_y_end_pt(self):
        return self._text_y_end

    def get_text_y_end_px(self):
        return self._unit_converter.pt_to_px(self.get_text_y_end_pt())

    def get_text_y_end_sp(self):
        return self._unit_converter.pt_to_sp(self.get_text_y_end_pt())


    def get_text_parindent_pt(self):
        return self._text_parindent

    def get_text_parindent_px(self):
        return self._unit_converter.pt_to_px(self._text_parindent)

    def get_text_parindent_sp(self):
        return self._unit_converter.pt_to_sp(self._text_parindent)


    def is_even_page(self, page_num):
        return page_num % 2 == 0
