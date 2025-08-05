from .latex_page_settings import LatexPageSettings

class LatexLandscapePageSettings(LatexPageSettings):

    def __init__(self):
        super().__init__()
        self._text_width = 430.00462
        self._text_height = 430.00462
