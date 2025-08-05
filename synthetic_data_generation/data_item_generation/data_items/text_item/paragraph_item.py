from pylatex import Document, NewLine, NoEscape
from pylatex.utils import escape_latex

from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.document_extension.command_extension.commands.log_paragraph_word_position_command import LogParagraphWordPositionCommand
from synthetic_data_generation.serializer.text_serializer.url_to_latex_url_serializer import UrlToLatexUrlSerializer
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.items_position_stores_manager import ItemsPositionStoresManager
from .text_item import TextItem
from synthetic_data_generation.data_item_generation.data_items.util.lang import is_latin_text, _wrap_latin_segments, wrap_latin_segments
import re

class ParagraphItem(TextItem):

    def __init__(self, index: int, data: dict):
        # Ensure we have text attribute before calling parent
        if 'text' not in data:
            data['text'] = ""
        
        # Initialize our own _text first as a safety measure
        self._text = data.get('text', '')
        
        super().__init__(index, data)
        self.first_word_logged = False

    def get_segment_text(
        self,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> dict:
        store = pos_stores_manager.get_paragraph_positions_store()
        positions = store.get_item_positions(self._index)
        try:
            temp = positions.get_substring(
                prov_item.get_page_num(), prov_item.get_page_col_bbox_index())
        except:
            print(f'problem with {prov_item.to_dict()}')

    def has_text_break(
        self,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> bool:
        store = pos_stores_manager.get_paragraph_positions_store()
        positions = store.get_item_positions(self._index)
        return positions.has_text_break(
            prov_item.get_page_num(), prov_item.get_page_col_bbox_index())

    def has_page_break(
        self,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> bool:
        store = pos_stores_manager.get_paragraph_positions_store()
        positions = store.get_item_positions(self._index)
        return positions.has_page_break(
            prov_item.get_page_num(), prov_item.get_page_col_bbox_index())

    def add_as_latex_to_doc(self, doc: Document):
        doc.append(NewLine())
        doc.log_write_position(self._index)
        self._add_latex_string_to_doc(doc)
        doc.log_write_position(self._index)
        doc.append(NewLine())

    def _add_latex_string_to_doc(self, doc: Document):
        latex_string = UrlToLatexUrlSerializer().urls_to_latex_urls(self._text)
        # Step 2: Wrap English segments with font and direction control
        latex_string = wrap_latin_segments(latex_string)
        for item in latex_string.split("<split>"):
            if (self._is_url(item)):
                self._add_url_string(item, doc)
            else:
                self._add_non_url_string(item, doc)

    def _is_url(self, string: str) -> bool:
        url_identifier = "url{"
        return (url_identifier in string)

    def _add_url_string(self, string: str, doc: Document):
        doc.append(NoEscape(string))
        if not self.first_word_logged:
            self._add_cmd_word_pos_log(string[5:-1], doc)
            self.first_word_logged = False

    def _add_non_url_string(self, string: str, doc: Document):
        if not self.first_word_logged:
            first_word = re.search(r'\b\w+\b', string)
            if first_word:
                self._add_cmd_word_pos_log(first_word.group(0), doc)
            self.first_word_logged = True
        doc.append(NoEscape(string + ' '))
            
    def _add_cmd_word_pos_log(self, string: str, doc: Document):
        doc.append(NoEscape(
            f"\\{LogParagraphWordPositionCommand().get_latex_name()}" +
            "{" + str(self._index) + "}"
            "{" + f"palabel{self._index}" + "}"
            "{" + string + "}"))
    
    def _split_long_words(self, word: str, language='en') -> list[str]:
        '''Split a word in subwords based on the distribution
           of word in the english dictionary
           https://medium.com/@davidxu90/relative-frequencies-of-words-in-the-english-language-94bf864a516c'''
        
        #take the word lenght that contains over the 95 words in the english dictionary
        word_p_95 = 15
        len_word = len(word)
        if len_word > word_p_95:
            word = word[:word_p_95]
        return word