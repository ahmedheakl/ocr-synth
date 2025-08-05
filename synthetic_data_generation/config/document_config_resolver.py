from synthetic_data_generation.config.config_keys import ConfigKeys
from synthetic_data_generation.config.config_values import ConfigValues
from synthetic_data_generation.document.document_selection.document_selector import DocumentSelector
from synthetic_data_generation.document.document_selection.available_document_selectors import AvailableDocumentSelectors

class DocumentConfigResolver:

    def resolve_doc_selection(self, config: dict) -> DocumentSelector:
        dataset_path = self._get_dataset_path(config)
        doc_selector = self._init_doc_selector(config, dataset_path)
        return doc_selector

    def _get_dataset_path(self, config: dict) -> str:
        if (self._has_dataset_path(config)):
            return config[ConfigKeys.DATASET_PATH]
        return ConfigValues.DATASET_PATH

    def _has_dataset_path(self, config: dict) -> bool:
        if (ConfigKeys.DATASET_PATH not in config):
            return False
        config_dataset_path = config[ConfigKeys.DATASET_PATH]
        return ((type(config_dataset_path) == str) and
            (config_dataset_path != ""))

    def _init_doc_selector(
        self, config: dict, dataset_path: str
    ) -> DocumentSelector:
        if (self._has_doc_selection(config)):
            # Only one key/value pair entry expected upon correct user input.
            doc_selection = config[ConfigKeys.DOCUMENT_SELECTION]
            for selector_type, selector_config in doc_selection.items():
                return AvailableDocumentSelectors.get_selector(
                    selector_type, selector_config, dataset_path)
        return AvailableDocumentSelectors.get_selector(
            ConfigKeys.SELECT_ALL, {}, dataset_path)

    def _has_doc_selection(self, config: dict) -> bool:
        return ((ConfigKeys.DOCUMENT_SELECTION in config) and
            (type(config[ConfigKeys.DOCUMENT_SELECTION]) == dict))
