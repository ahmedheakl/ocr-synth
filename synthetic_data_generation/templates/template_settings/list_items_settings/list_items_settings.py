import random
from pylatex import Enumerate, Itemize
from pylatex.base_classes import Environment

from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class ListItemsSettings:

    _type_item = "item"
    _type_enum = "enumerate"
    _type_random = "random"

    def __init__(self, config_data: dict):
        list_items_config = config_data.get(TemplateKeys.LIST_ITEMS, {})
        self._type = list_items_config.get(
            TemplateKeys.LIST_ITEM_TYPE, ListItemsSettings._type_random)
        self._symbol = self._resolve_symbol(list_items_config)

    def gen_env(self) -> Environment:
        if (self._type == ListItemsSettings._type_item):
            return Itemize()
        elif (self._type == ListItemsSettings._type_enum):
            return Enumerate(enumeration_symbol=self._symbol)
        return self._gen_random_env()

    def _gen_random_env(self) -> Environment:
        env_classes = [Itemize, Enumerate]
        index_random = random.randint(0, len(env_classes) - 1)
        env_class = env_classes[index_random]
        if (env_class == Itemize):
            return Itemize()
        return Enumerate(enumeration_symbol=self._gen_random_enum_symbol())

    def _gen_random_enum_symbol(self) -> str:
        return random.choice([None, "\\alph*.", "\\alph*)", "\\alph*.)"])

    def _resolve_symbol(self, config_data: dict) -> str:
        symbol = config_data.get(TemplateKeys.LIST_ITEM_SYMBOL, None)
        if ((symbol is None) or (type(symbol) != str) or (symbol == "")):
            return None
        return "\\" + symbol
