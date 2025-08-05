import random

from synthetic_data_generation.config.config_keys import ConfigKeys
from .document_selector import DocumentSelector

class RandomDocumentSelector(DocumentSelector):

    _num_to_select_default = 1

    def __init__(self, config: dict, dataset_path: str):
        super().__init__(dataset_path)
        self._num_to_select = self._resolve_num_to_select(config)

    def select_doc_file_names(self) -> list[str]:
        return sorted(random.sample(
            self._get_all_doc_file_names(), self._num_to_select))

    def _resolve_num_to_select(self, config: dict) -> int:
        if ((type(config) == dict) and (ConfigKeys.NUM_TO_SELECT in config)):
            num_to_select = config[ConfigKeys.NUM_TO_SELECT]
            if (type(num_to_select) == int):
                return num_to_select
        return self._num_to_select_default
