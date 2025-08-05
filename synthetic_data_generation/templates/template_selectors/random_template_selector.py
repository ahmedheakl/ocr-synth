import random

from synthetic_data_generation.config.config_keys import ConfigKeys
from .template_creation_info import TemplateCreationInfo
from .template_selector import TemplateSelector

class RandomTemplateSelector(TemplateSelector):

    _num_to_select_default = 1

    def __init__(self, template_type: str, config: dict):
        super().__init__(template_type, config)
        self._num_to_select = self._resolve_num_to_select(config)

    def select_template_creation_infos(self) -> list[TemplateCreationInfo]:
        template_creation_infos = self._gen_template_creation_infos()
        return self._sample_template_creation_infos(template_creation_infos)

    def _gen_template_creation_infos(self) -> list[TemplateCreationInfo]:
        data = []
        sampled_template_file_paths = random.sample(
            self._get_all_template_file_paths(), self._num_to_select)
        for template_file_path in sampled_template_file_paths:
            template_data = self._data_loader.load_json_data(
                template_file_path)
            data.append(TemplateCreationInfo(
                self._template_type, self._num_instances, template_data))
        return data

    def _resolve_num_to_select(self, config: dict) -> int:
        if (ConfigKeys.NUM_TO_SELECT in config):
            return config[ConfigKeys.NUM_TO_SELECT]
        return self._num_to_select_default
