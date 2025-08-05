from synthetic_data_generation.templates.available_options.available_items import AvailableItems
from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class ActiveItems:

    def __init__(self, template: dict):
        self._items_status = self._gen_items_status(template)

    def has_item(self, item: str) -> bool:
        if (item in self._items_status):
            return self._items_status[item]
        return False

    def _gen_items_status(self, template: dict) -> dict:
        items_status = self._gen_items_status_default()
        self._set_inactive_items(items_status, template)
        return items_status

    def _gen_items_status_default(self) -> dict[str, bool]:
        return {item: True for item in AvailableItems.get_items()}

    def _set_inactive_items(self, items_status: dict, template: dict):
        if not self._template_has_inactive_items(template): return
        for inactive_item in template[TemplateKeys.INACTIVE_ITEMS]:
            if (inactive_item in items_status):
                items_status[inactive_item] = False

    def _template_has_inactive_items(self, template: dict) -> bool:
        return (TemplateKeys.INACTIVE_ITEMS in template)
