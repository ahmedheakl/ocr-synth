from synthetic_data_generation.config.config_keys import ConfigKeys
from .document_selector import DocumentSelector

class CustomDocumentSelector(DocumentSelector):

    def __init__(self, config: dict, dataset_path: str):
        super().__init__(dataset_path)
        self._selected_doc_file_names = self._resolve_selected_doc_file_names(
            config)

    def select_doc_file_names(self) -> list[str]:
        return self._selected_doc_file_names

    def _resolve_selected_doc_file_names(self, config: dict) -> list[str]:
        if (self._has_doc_file_names_item(config)):
            doc_file_names = sorted(config[ConfigKeys.DOCUMENT_FILE_NAMES])
            if (self._are_doc_file_names_valid(doc_file_names)):
                return doc_file_names
        return []

    def _has_doc_file_names_item(self, config: dict) -> bool:
        return ((type(config) == dict) and
            (ConfigKeys.DOCUMENT_FILE_NAMES in config))

    def _are_doc_file_names_valid(self, doc_file_names: list) -> bool:
        if (type(doc_file_names) != list):
            return False
        for doc_file_name in doc_file_names:
            if (type(doc_file_name) != str):
                return False
        return True
