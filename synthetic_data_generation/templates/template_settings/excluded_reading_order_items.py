from synthetic_data_generation.templates.available_options.available_items import AvailableItems
from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class ExcludedReadingOrderItems:

    def __init__(self, template: dict):
        self._items = self._gen_excluded_items(template)

    def has_item(self, item: str) -> bool:
        return (item in self._items)

    def _gen_excluded_items(self, template: dict) -> list[str]:
        excluded_items = []
        if not (self._template_has_entry(template)):
            return excluded_items
        available_items = AvailableItems.get_items()
        excluded_template_items = template[
            TemplateKeys.EXCLUDED_READING_ORDER_ITEMS]
        for available_item in available_items:
            if (available_item in excluded_template_items):
                excluded_items.append(available_item)
        return excluded_items

    def _template_has_entry(self, template: dict) -> bool:
        return (TemplateKeys.EXCLUDED_READING_ORDER_ITEMS in template)
