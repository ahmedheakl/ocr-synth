class UnitConverter:

    def __init__(self):
        self._pt_to_px_ratio = 4 / 3
        self._px_to_pt_ration = 1 / self._pt_to_px_ratio
        self._sp_to_pt_ratio = 1 / 65536
        self._pt_to_sp_ratio = 1 / self._sp_to_pt_ratio
        self._in_to_pt_ratio = 72
        self._pt_to_in_ratio = 1 / self._in_to_pt_ratio
        self._in_to_cm_ratio = 2.54
        self._cm_to_in_ratio = 1 / self._in_to_cm_ratio
        self._mm_to_cm_ratio = 0.1

    def sp_to_pt(self, value):
        return self._sp_to_pt_ratio * value

    def sp_to_px(self, value):
        return self.pt_to_px(self.sp_to_pt(value))

    def px_to_pt(self, value):
        return self._px_to_pt_ration * value

    def px_to_sp(self, value):
        return self.pt_to_sp(self.px_to_pt(value))

    def px_to_cm(self, value):
        return self.pt_to_in(self.px_to_pt(value)) * self._in_to_cm_ratio

    def pt_to_px(self, value):
        return round(self._pt_to_px_ratio * value)

    def pt_to_sp(self, value):
        return int(self._pt_to_sp_ratio * value)

    def pt_to_in(self, value):
        return value * self._pt_to_in_ratio

    def in_to_pt(self, value):
        return value * self._in_to_pt_ratio

    def mm_to_pt(self, value):
        return self.in_to_pt(
            value * self._mm_to_cm_ratio * self._cm_to_in_ratio)
