import re

from synthetic_data_generation.data_cleaning.text_cleaner import TextCleaner
from synthetic_data_generation.data_item_generation import ccs_to_doclaynet_map
from synthetic_data_generation.serializer import data_to_latex_type_serializer as Serializer
from util.latex_item_type_names import LatexItemTypeNames
from .util.prov import Prov
from util.retrieve_index_from_reference import retrieve_index_type_from_reference_string
import time

class MainTextItem:

    def __init__(self, index, data: dict):
        self._index = index
        self._type = data.get("label", "")  # Use .get() with default
        
        # Initialize _text first with a default value
        self._text = ""
        
        try:
            index, type_ref = retrieve_index_type_from_reference_string(data.get('self_ref', ''))
            self._ref_type = type_ref
        except:
            self._ref_type = 'texts'  # Default fallback
            
        if self._ref_type == 'groups':
            #Groups don't have any prov information, and as well the components inside
            empty_prova_data = self._generate_empty_prov_data()
            self._prov = Prov(empty_prova_data)
        else:
            self._prov = Prov(data.get("prov", []))  # Use .get() with default
            
        # Set _text after initialization, with proper fallback
        if "text" in data and data["text"]:
            self._text = TextCleaner().clean_text(data["text"])
        else:
            self._text = ""
            
        self._is_list_item = (
            data.get("name", "") == LatexItemTypeNames.LIST_ITEM)
        
        self._is_caption = False
    
    def is_valid(self):
        return True
    
    def _generate_empty_prov_data(self):
        prov_list = []
        return prov_list

    def get_index(self) -> int:
        return self._index

    def get_type(self) -> str:
        return self._type

    def get_label(self) -> str:
        return ccs_to_doclaynet_map.ccs_to_doclay_net_type(self._type)

    def get_prov(self) -> Prov:
        return self._prov

    def get_text(self) -> str:
        return self._text
    
    def get_self_ref_type(self) -> str:
        return self._ref_type

    def get_segment_text(self, *args) -> str:
        return None if (self._text == "") else self._text

    def get_segment_data(self, *args) -> list:
        return []

    def has_text(self) -> bool:
        return (self._text != "")

    def has_text_break(self, *args) -> bool:
        return False

    def has_page_break(self, *args) -> bool:
        return False

    def is_section(self) -> bool:
        return Serializer.is_a_section_type(self._type)

    def is_page_header(self) -> bool:
        return Serializer.is_page_header(self._type)

    def is_title(self) -> bool:
        return Serializer.is_title(self._type)

    def is_list_item(self) -> bool:
        return self._is_list_item
    
    def is_caption(self):
        return self._is_caption

    def escape_special_latex_chars(self, string: str) -> str:
        string = re.sub(r"\\", r"\\textbackslash ", string)
        string = re.sub(r"\~", r"\\textasciitilde ", string)
        string = re.sub(r"\^", r"\\textasciicircum ", string)
        string = re.sub(r"\&", r"\&", string)
        string = re.sub(r"\$", r"\$", string)
        string = re.sub(r"\#", r"\#", string)
        string = re.sub(r"\_", r"\_", string)
        string = re.sub(r"\{", r"\{", string)
        string = re.sub(r"\}", r"\}", string)
        return string