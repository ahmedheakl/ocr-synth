from synthetic_data_generation.config.config_keys import ConfigKeys
from .template_selector import TemplateSelector
from .all_template_selector import AllTemplateSelector
from .custom_template_selector import CustomTemplateSelector
from .random_template_selector import RandomTemplateSelector
from .null_template_selector import NullTemplateSelector

class AvailableTemplateSelectors:

    _table = {
        ConfigKeys.SELECT_ALL: AllTemplateSelector,
        ConfigKeys.SELECT_CUSTOM: CustomTemplateSelector,
        ConfigKeys.SELECT_RANDOM: RandomTemplateSelector
    }

    def get_selector(
        template_type: str, template_type_config: dict
    ) -> TemplateSelector:
        # Only one key/value pair is expected upon correct user input.
        if (type(template_type_config) == dict):
            for selector_type, config in template_type_config.items():
                if (selector_type in AvailableTemplateSelectors._table):
                    selector = AvailableTemplateSelectors._table[selector_type]
                    return selector(template_type, config)
        return NullTemplateSelector()
