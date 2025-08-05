from synthetic_data_generation.templates.available_options.available_font_colors import AvailableFontColors
from synthetic_data_generation.templates.available_options.available_font_sizes import AvailableFontSizes
from synthetic_data_generation.templates.available_options.available_font_styles import AvailableFontStyles
from synthetic_data_generation.templates.util.font_style import FontStyle
from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.util.template_values import TemplateValues

class StyleItem:

    _default_item_position = "c"
    _valid_item_positions = [
        "",
        "l",
        "r",
        _default_item_position,
        TemplateKeys.RANDOM
    ]
    _default_cell_position = "c"
    _valid_cell_positions = [
        "l",
        "r",
        _default_cell_position,
        TemplateKeys.RANDOM
    ]

    def __init__(self, item_config: dict, layout_config: dict):
        self._font_color = self._resolve_font_color(item_config, layout_config)
        self._font_size = self._resolve_font_size(item_config, layout_config)
        self._font_style = self._resolve_font_style(item_config, layout_config)
        self._size = self._resolve_size(item_config)
        self._position = self._resolve_position(item_config)
        self._cell_position = self._resolve_cell_position(item_config)

    def get_font_color(self) -> str:
        return self._font_color

    def get_font_size(self) -> int:
        return self._font_size

    def get_font_style(self) -> FontStyle:
        return self._font_style

    def get_size(self) -> int:
        return self._size

    def get_position(self) -> str:
        return self._position

    def get_cell_position(self) -> str:
        return self._cell_position

    def _resolve_font_color(
        self, item_config: dict, layout_config: dict
    ) -> str:
        if (self._has_entry(item_config, TemplateKeys.FONT_COLOR)):
            return AvailableFontColors.get_this_or_default_color(
                item_config[TemplateKeys.FONT_COLOR])
        return None

    def _resolve_font_size(self, item_config: dict, layout_config: dict) -> int:
        if (self._has_entry(item_config, TemplateKeys.FONT_SIZE)):
            return AvailableFontSizes.get_this_or_default_size_as_int(
                item_config[TemplateKeys.FONT_SIZE])
        return None

    def _resolve_font_style(
        self, item_config: dict, layout_config: dict
    ) -> FontStyle:
        if (self._has_entry(item_config, TemplateKeys.FONT_STYLE)):
            return AvailableFontStyles.font_style_to_instance(
                item_config[TemplateKeys.FONT_STYLE])
        return None

    def _resolve_size(self, item_config: dict) -> int:
        if (self._has_entry(item_config, TemplateKeys.ITEM_SIZE)):
            template_item_size = item_config[TemplateKeys.ITEM_SIZE]
            if (self._is_size_valid(template_item_size)):
                return template_item_size
        return TemplateValues.SIZE_DEFAULT

    def _is_size_valid(self, size: int) -> bool:
        if (type(size) != int):
            return False
        if (TemplateValues.is_random_identifier_int(size)):
            return True
        return ((size >= TemplateValues.SIZE_MIN) and
            (size <= TemplateValues.SIZE_MAX))

    def _resolve_position(self, item_config: dict) -> str:
        if (self._has_entry(item_config, TemplateKeys.POSITION)):
            template_position = item_config[TemplateKeys.POSITION]
            if (type(template_position) != str):
                return StyleItem._default_item_position
            if (template_position in StyleItem._valid_item_positions):
                return template_position
        return StyleItem._default_item_position

    def _resolve_cell_position(self, item_config: dict) -> int:
        if (self._has_entry(item_config, TemplateKeys.CELL_POSITION)):
            template_cell_position = item_config[TemplateKeys.CELL_POSITION]
            if (template_cell_position in StyleItem._valid_cell_positions):
                return template_cell_position
        return StyleItem._default_cell_position

    def _has_entry(self, item_config: dict, key: str) -> bool:
        return (key in item_config)
