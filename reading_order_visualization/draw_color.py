class DrawColor:

    def __init__(self):
        self._dark_blue = (0, 0, 204)
        self._light_blue = (77, 184, 255)

    def get_color(self, cnt):
        if (self._cnt_is_even(cnt)):
            return self._dark_blue
        return self._light_blue
    
    def _cnt_is_even(self, cnt):
        return (cnt % 2 == 0)
