from data_loading.data_loader import DataLoader
from synthetic_data_generation.templates.util.position_item import PositionItem
from synthetic_data_generation.templates.util.style_item import StyleItem
from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class TemplateQuestioner:

    def __init__(self, template: dict):
        self._template = template

    def get_layout_style(self) -> dict:
        base_layout_style = self._load_base_layout_style()
        template_layout_style = self._get_template_layout_style()
        layout_style = self._merge_base_with_template_layout_style(
            base_layout_style, template_layout_style)
        return layout_style

    def _load_base_layout_style(self) -> dict:
        path = ("./synthetic_data_generation/templates/template_settings/"
            "layout_settings/")
        file_name = "base_layout_style.json"
        file_path = path + file_name
        return DataLoader().load_json_data(file_path)

    def _get_template_layout_style(self) -> dict:
        if (self._has_template_layout_style()):
            return self._template[TemplateKeys.LAYOUT_STYLE]
        return {}

    def _has_template_layout_style(self) -> bool:
        return ((TemplateKeys.LAYOUT_STYLE in self._template) and
            (type(self._template[TemplateKeys.LAYOUT_STYLE]) == dict))

    def _merge_base_with_template_layout_style(
        self, base_layout_style: dict, template_layout_style: dict
    ):
        for key in base_layout_style:
            if (self._has_template_layout_value(key, base_layout_style,
                template_layout_style)):
                base_layout_style[key] = template_layout_style[key]
        return base_layout_style

    def _has_template_layout_value(
        self, key: str, base_layout_style: dict, template_layout_style: dict
    ) -> bool:
        if not (key in template_layout_style):
            return False
        base_value_type = type(base_layout_style[key])
        template_value_type = type(template_layout_style[key])
        if (self._are_values_numbers(base_value_type, template_value_type)):
            return True
        return (base_value_type == template_value_type)

    def _are_values_numbers(
        self, base_value_type, template_value_type
    ) -> bool:
        is_base_value_number = ((base_value_type == int) or
            (base_value_type == float))
        is_template_value_number = ((template_value_type == int) or
            (template_value_type == float))
        return (is_base_value_number and is_template_value_number)

    def get_watermark_style(self) -> dict:
        if (TemplateKeys.WATERMARKS_STYLE in self._template):
            config = self._template[TemplateKeys.WATERMARKS_STYLE]
            if (type(config) == dict):
                return config
        return {}

    def get_line_nums_config(self) -> dict:
        if (TemplateKeys.LINE_NUMS in self._template):
            config = self._template[TemplateKeys.LINE_NUMS]
            if (type(config) == dict):
                return config
        return {}

    def get_figure_position_item(self) -> PositionItem:
        return self._get_position_item(TemplateKeys.FIGURE_ITEM)

    def get_table_position_item(self) -> PositionItem:
        return self._get_position_item(TemplateKeys.TABLE_ITEM)

    def _get_position_item(self, item_type: str) ->  PositionItem:
        try:
            type_items = self._get_type_items(TemplateKeys.ITEM_POSITION)
            type_item = self._get_type_item(type_items, item_type)
            return PositionItem(type_item)
        except:
            return PositionItem()

    def get_figure_style_item(self, pos_type: str) -> StyleItem:
        return self._get_style_item(TemplateKeys.FIGURE_ITEM, pos_type)

    def get_table_style_item(self, pos_type: str) -> StyleItem:
        return self._get_style_item(TemplateKeys.TABLE_ITEM, pos_type)

    def get_text_style_item(self, pos_type: str) -> StyleItem:
        return self._get_style_item(TemplateKeys.TEXT_ITEM, pos_type)

    def _get_style_item(self, item_type: str, pos_type: str) -> StyleItem:
        style_item = self._get_template_style_item(item_type, pos_type)
        layout_style = self._get_template_layout_style()
        return StyleItem(style_item, layout_style)

    def _get_template_style_item(self, item_type: str, pos_type: str) -> dict:
        try:
            type_items = self._get_type_items(TemplateKeys.ITEM_STYLE)
            type_item = self._get_type_item(type_items, item_type)
            style_item = self._get_type_item_item(type_item, pos_type)
            return style_item
        except:
            return {}

    def _get_type_items(self, item_category: str) -> dict:
        return self._template[item_category]

    def _get_type_item(self, type_items: dict, item_type: str) -> dict:
        return type_items[item_type]

    def _get_type_item_item(self, type_item: dict, pos_type: str) -> dict:
        return type_item[pos_type]
