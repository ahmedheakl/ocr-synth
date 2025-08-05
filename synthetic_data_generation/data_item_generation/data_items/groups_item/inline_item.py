from pylatex import NewLine, Math
from pylatex.utils import NoEscape
from pylatex import Figure, NewLine, NoEscape, SubFigure

from synthetic_data_generation.data_item_generation.data_items.main_text_item import MainTextItem
from synthetic_data_generation.data_item_generation.data_items.text_item.text_item import TextItem
from synthetic_data_generation.document_extension.command_extension.commands.log_paragraph_word_position_command import LogParagraphWordPositionCommand
from synthetic_data_generation.document_generation.data_stores_manager import DataStoresManager
from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.serializer.text_serializer.url_to_latex_url_serializer import UrlToLatexUrlSerializer
from util.data_stores.docling_data_store import DoclingDataStore
from util.retrieve_index_from_reference import retrieve_index_type_from_reference_string, retrieve_component_from_index_and_type

from synthetic_data_generation.data_structures.latex_document.custom_document import CustomDocument
from synthetic_data_generation.templates.template import Template
from util.latex_item_type_names import LatexItemTypeNames
import time
import re

class InlineItem(MainTextItem):
    """
    Item representing the Inline group. this group contains code, text and formulas all aligned
    in the same paragraph.
    """
    def __init__(self, index, data: dict):
        super().__init__(index, data)
        # Optionally, you might check that the label is one that you expect for equations:
        if data.get("label") != LatexItemTypeNames.INLINE:
            raise ValueError("INLINEItem must have a formula label")
        self._childrens = data.get('children', [])
        self._docling_data_store = DoclingDataStore()
        self._inline_group_index = index
        self.first_word_logged = False
    
    def get_children_ref_list(self) -> list:
        children_ref = [child['$ref'] for child in self._childrens]
        return children_ref
    
    def get_children_ref_dict(self) -> dict:
        return self._childrens
    
    def get_children_item(self) -> list:
        children_item = []
        children_ref = self.get_children_ref_list()
        for child_ref in children_ref:
            index, type_ref = retrieve_index_type_from_reference_string(child_ref)
            item = retrieve_component_from_index_and_type(index, type_ref)
            children_item.append(item)
        return children_item
    
    def get_latex_text(self):
        children_ref = self.get_children_ref_list()
        final_text = ""
        for child_ref in children_ref:
            index, type_ref = retrieve_index_type_from_reference_string(child_ref)
            item = retrieve_component_from_index_and_type(index, type_ref)
            text = item['text']
            label = item['label']
            if 'formula' in label:
                final_text += self._add_inline_equation_to_string(text)
            else:
                final_text += self._add_inline_text_to_string(text)
        return final_text

    def add_as_latex_to_doc(self, doc: CustomDocument):
        """
        Add the inline group inside the document. For now only formula and standard 
        text are supported. The inline groups have a empty provenence, therefore the
        log of the position is not needed.
        """
        #In case you need to add the provenence field, remove the comment from the log_write_position
        #this will consider the bounding box for the entire group. If you want the bounding box of
        #each children, you need to log and and to ItemStore each component.

        # Insert a new line before the equation
        doc.append(NewLine())
        doc.log_write_position(self._index)
        children_ref = self.get_children_ref_list()
        for child_ref in children_ref:
            index, type_ref = retrieve_index_type_from_reference_string(child_ref)
            item = retrieve_component_from_index_and_type(index, type_ref)
            text = item['text']
            label = item['label']
            if 'formula' in label:
                self._add_inline_equation_to_doc(doc, text)
            else:
                self._add_inline_text_to_doc(doc, text)
        doc.log_write_position(self._index)
        doc.append(NewLine())
        print("adding formula inline")
        # Log the write position if the item is meant to be included in the reading order.
        excluded_ro_items = Template().get_excluded_reading_order_items()
        # if not excluded_ro_items.has_item(self._type):
    
    def _add_inline_equation_to_doc(self, doc: CustomDocument, text):
        '''add an inline equation to the current document'''
        doc.append(NoEscape(r"$ " + text + r" $"))
        # print("added inline formula")
    
    def _add_inline_equation_to_string(self, text: str):
        return "$ " + text + " $ "
    
    def _add_inline_text_to_doc(self, doc: CustomDocument, text: str):
        self._add_latex_string_to_doc(doc, text)

    def _add_inline_text_to_string(self, text: str):
        latex_string = UrlToLatexUrlSerializer().urls_to_latex_urls(text)
        string = ""
        for item in latex_string.split("<split>"):
            if (self._is_url(item)):
                string += latex_string + " " 
            else:
                 for word in latex_string.split(" "):
                    latex_word = self.escape_special_latex_chars(word)
                    latex_words = self._split_long_words(latex_word)
                    string += latex_words + " "
        return string

    def _add_latex_string_to_doc(self, doc: CustomDocument, text: str):
        latex_string = UrlToLatexUrlSerializer().urls_to_latex_urls(text)
        for item in latex_string.split("<split>"):
            if (self._is_url(item)):
                self._add_url_string(item, doc)
            else:
                self._add_non_url_string(item, doc)

    def _is_url(self, string: str) -> bool:
        url_identifier = "url{"
        return (url_identifier in string)

    def _add_url_string(self, string: str, doc: CustomDocument):
        doc.append(NoEscape(string))

    def _add_non_url_string(self, string: str, doc: CustomDocument):
        end_of_line_marker = "%"
        print('adding non url string')
        for i, word in enumerate(string.split(" ")):
            latex_word = self.escape_special_latex_chars(word)
            latex_word = self._split_long_words(latex_word)
            doc.append(NoEscape(latex_word + " " +  end_of_line_marker))
            if not self.first_word_logged:
                self._add_cmd_word_pos_log(word, doc)
                self.first_word_logged = True
            doc.append(NoEscape(" " + end_of_line_marker))
        
    def _add_cmd_word_pos_log(self, string: str, doc: CustomDocument):
        doc.append(NoEscape(
            f"\\{LogParagraphWordPositionCommand().get_latex_name()}" +
            "{" + str(self._inline_group_index) + "}"
            "{" + f"palabel{self._index}" + "}"
            "{" + string + "}"))
    
    def set_caption(self):
        self._is_caption = True

    def is_caption(self):
        return self._is_caption
    
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

        
