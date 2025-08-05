from .text_item import TextItem

class CaptionItem(TextItem):

    def __init__(self, index, data: dict):
        super().__init__(index, data)
    
    def add_as_latex_to_doc(self, doc):
        # Captions are added by the items that own them (e.g. FigureItem).
        # This item only exists to have a one-to-one mapping from each ccs
        # item to a class instance. This preserves the correct sequence.
        pass
