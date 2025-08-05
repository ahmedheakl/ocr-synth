import re

from synthetic_data_generation.data_item_generation.data_items.main_text_item import MainTextItem

class TextItem(MainTextItem):

    def __init__(self, index, data: dict):
        # Ensure _text is initialized before calling super().__init__
        # This is a defensive measure in case super().__init__ references _text
        if not hasattr(self, '_text'):
            self._text = ""
        
        # Fix the prov data before calling super
        if 'prov' in data and len(data['prov']) > 0:
            for i, prov in enumerate(data['prov']):
                # Ensure charspan exists and has proper values
                if 'charspan' not in prov:
                    text_len = len(data.get('text', ''))
                    data['prov'][i]['charspan'] = (0, text_len)
                elif not prov['charspan'] or len(prov['charspan']) != 2:
                    text_len = len(data.get('text', ''))
                    data['prov'][i]['charspan'] = (0, text_len)
        else:
            # Add default prov if missing
            text_len = len(data.get('text', ''))
            data['prov'] = [{
                'bbox': [0, 0, 100, 20],
                'page_no': 1,
                'charspan': (0, text_len)
            }]
        
        # Now call the parent constructor
        super().__init__(index, data)

    def get_text(self):
        return super().get_text()

    def _split_long_unbreakable_char_sequences(self, text):
        return re.sub(r"([^ -]{16})", r"\1\ ", text)
    
    def get_latex_text(self):
        return self._text
    
    def set_caption(self):
        self._is_caption = True

    def is_caption(self):
        return self._is_caption