from synthetic_data_generation.config.config_keys import ConfigKeys
from synthetic_data_generation.templates.template_selectors.available_template_selectors import AvailableTemplateSelectors
from synthetic_data_generation.templates.template_selectors.null_template_selector import NullTemplateSelector
from synthetic_data_generation.templates.template_selectors.template_selectors import TemplateSelectors

class TemplateConfigResolver:

    def resolve_templates(self, config: dict) -> TemplateSelectors:
        if not (self._has_template_selection_data(config)):
            self._raise_missing_template_selection_error()
        return self._read_template_config(config)

    def _has_template_selection_data(self, config: dict) -> bool:
        return (ConfigKeys.TEMPLATE_SELECTION in config)

    def _raise_missing_template_selection_error(self):
        raise ValueError(
            f"[ERROR] The key '{ConfigKeys.TEMPLATE_SELECTION}' is "
            "missing in config.json!")

    def _read_template_config(self, config: dict) -> TemplateSelectors:
        template_selectors = {}
        template_selection = config[ConfigKeys.TEMPLATE_SELECTION]
        for template_category in self._gen_template_categories():
            if (template_category in template_selection):
                template_selector = AvailableTemplateSelectors.get_selector(
                    template_category, template_selection[template_category])
                template_selectors[template_category] = template_selector
            else:
                template_selectors[template_category] = NullTemplateSelector()
        return TemplateSelectors(template_selectors)

    def _gen_template_categories(self) -> list[str]:
        return [
            ConfigKeys.OFFICIAL_TEMPLATES,
            ConfigKeys.INTERNAL_TEMPLATES,
            ConfigKeys.PERSONAL_TEMPLATES
        ]
