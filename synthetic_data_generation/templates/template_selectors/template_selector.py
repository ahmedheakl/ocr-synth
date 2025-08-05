import glob
import random

from data_loading.data_loader import DataLoader
from synthetic_data_generation.config.config_keys import ConfigKeys
from synthetic_data_generation.config.config_values import ConfigValues
from .template_creation_info import TemplateCreationInfo

class TemplateSelector:

    _num_instances_default = 1
    _num_instances_min = 1
    _num_instances_max = 10

    def __init__(self, template_type: str, config: dict):
        self._template_type = template_type
        self._num_to_shuffle = self._resolve_num_to_shuffle(config)
        self._num_instances = self._resolve_num_instances(config)
        self._data_loader = DataLoader()

    def _sample_template_creation_infos(
        self, template_creation_infos: list[TemplateCreationInfo]
    ) -> list[TemplateCreationInfo]:
        if ((self._num_to_shuffle == 0) or
            (len(template_creation_infos) < self._num_to_shuffle)):
            return template_creation_infos
        return random.sample(
            template_creation_infos, self._num_to_shuffle)

    def _get_all_template_file_paths(self) -> list[str]:
        dir_path = self._gen_template_dir_path()
        return glob.glob(f"{dir_path}*.json")

    def _gen_template_dir_path(self):
        return ConfigValues.TEMPLATES_PATH + self._template_type + "/"

    def _resolve_num_to_shuffle(self, config: dict) -> int:
        if (ConfigKeys.NUM_TO_SHUFFLE in config):
            num_to_shuffle = config[ConfigKeys.NUM_TO_SHUFFLE]
            if ((type(num_to_shuffle) == int) and (num_to_shuffle > 0)):
                return num_to_shuffle
        return 0

    def _resolve_num_instances(self, config: dict) -> int:
        if (ConfigKeys.NUM_INSTANCES in config):
            return self._clip_num_instances(config[ConfigKeys.NUM_INSTANCES])
        return self._num_instances_default

    def _clip_num_instances(self, num_instances: int) -> int:
        return max(min(num_instances, self._num_instances_max),
            self._num_instances_min)
