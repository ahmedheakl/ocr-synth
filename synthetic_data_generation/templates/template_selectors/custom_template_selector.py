from synthetic_data_generation.config.config_keys import ConfigKeys
from util import file_path_manager
from .template_creation_info import TemplateCreationInfo
from .template_selector import TemplateSelector

class CustomTemplateSelector(TemplateSelector):

    def __init__(self, template_type: str, config: dict):
        super().__init__(template_type, config)
        self._template_names_to_select = (
            self._resolve_template_names_to_select(config))

    def select_template_creation_infos(self) -> list[TemplateCreationInfo]:
        template_creation_infos = self._gen_template_creation_infos()
        return self._sample_template_creation_infos(template_creation_infos)

    def _gen_template_creation_infos(self) -> list[TemplateCreationInfo]:
        data = []
        for template_file_path in self._get_all_template_file_paths():
            if (self._is_selected_template(template_file_path)):
                data.append(self._gen_template_creation_info(
                    template_file_path))
        return data

    def _is_selected_template(self, template_file_path: str) -> bool:
        template_name = file_path_manager.extract_fname_with_ext(
            template_file_path)
        for template_name_to_select in self._template_names_to_select:
            if (template_name_to_select == template_name):
                return True
        return False

    def _gen_template_creation_info(
        self, template_file_path: str
    ) -> TemplateCreationInfo:
        template_data = self._data_loader.load_json_data(template_file_path)
        return TemplateCreationInfo(
            self._template_type, self._num_instances, template_data)

    def _resolve_template_names_to_select(self, config: dict) -> list[str]:
        template_names_to_select = []
        if ((type(config) == dict) and (ConfigKeys.TEMPLATE_NAMES in config)):
            template_names = config[ConfigKeys.TEMPLATE_NAMES]
            if (type(template_names) != list):
                return template_names_to_select
            for template_name in template_names:
                if (self._is_template_name_valid(template_name)):
                    template_names_to_select.append(template_name)
        return template_names_to_select

    def _is_template_name_valid(self, template_name: str) -> bool:
        extension = file_path_manager.extract_file_ext(template_name)
        return (extension == "json")
