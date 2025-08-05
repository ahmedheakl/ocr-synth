from synthetic_data_generation.config.config_keys import ConfigKeys
from synthetic_data_generation.templates.template_selectors.template_creation_info import TemplateCreationInfo

class TemplateSelectors:

    def __init__(self, template_selectors: dict):
        self._official_selector = template_selectors[
            ConfigKeys.OFFICIAL_TEMPLATES]
        self._internal_selector = template_selectors[
            ConfigKeys.INTERNAL_TEMPLATES]
        self._personal_selector = template_selectors[
            ConfigKeys.PERSONAL_TEMPLATES]

    def select_template_creation_infos(self) -> list[TemplateCreationInfo]:
        templates = []
        templates += self._official_selector.select_template_creation_infos()
        templates += self._internal_selector.select_template_creation_infos()
        templates += self._personal_selector.select_template_creation_infos()
        return templates
