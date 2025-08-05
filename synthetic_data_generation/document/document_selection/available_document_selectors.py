from synthetic_data_generation.config.config_keys import ConfigKeys
from .document_selector import DocumentSelector
from .all_document_selector import AllDocumentSelector
from .custom_document_selector import CustomDocumentSelector
from .random_document_selector import RandomDocumentSelector

class AvailableDocumentSelectors:

    _table = {
        ConfigKeys.SELECT_ALL: AllDocumentSelector,
        ConfigKeys.SELECT_CUSTOM: CustomDocumentSelector,
        ConfigKeys.SELECT_RANDOM: RandomDocumentSelector
    }

    def get_selector(
        selector_type: str, selector_config: dict, dataset_path: str
    ) -> DocumentSelector:
        if (selector_type in AvailableDocumentSelectors._table):
            selector = AvailableDocumentSelectors._table[selector_type]
            return selector(selector_config, dataset_path)
        return AllDocumentSelector(selector_config, dataset_path)
