from random import choice

from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class PositionItem:

    _positions = [
        TemplateKeys.ONE_COL_POSITION,
        TemplateKeys.ALL_COL_POSITION,
        TemplateKeys.WRAP_POSITION
    ]

    def __init__(self, item_config: dict=None):
        item_config = item_config if (type(item_config) == dict) else {}
        self._pos_type = self._resolve_pos_type(item_config)

    def get_pos_type(self) -> str:
        if (self._pos_type == TemplateKeys.RANDOM):
            return choice(PositionItem._positions)
        return self._pos_type

    def _resolve_pos_type(self, item_config: dict) -> str:
        if (self._is_one_pos_type_active(item_config)):
            return self._get_active_pos_type(item_config)
        return TemplateKeys.ONE_COL_POSITION

    def _is_one_pos_type_active(self, item_config: dict) -> bool:
        num_active_pos_types = 0
        for position in PositionItem._positions:
            if ((position in item_config) and (item_config[position])):
                num_active_pos_types += 1
        if ((TemplateKeys.RANDOM in item_config) and
            (item_config[TemplateKeys.RANDOM])):
            num_active_pos_types += 1
        return num_active_pos_types == 1        

    def _get_active_pos_type(self, item_config: dict) -> str:
        for position in PositionItem._positions:
            if (item_config[position]):
                return position
        return TemplateKeys.RANDOM
