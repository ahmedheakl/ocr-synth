from .template_creation_info import TemplateCreationInfo
from .template_selector import TemplateSelector

class AllTemplateSelector(TemplateSelector):

    def __init__(self, template_type: str, config: dict):
        super().__init__(template_type, config)

    def select_template_creation_infos(self) -> list[TemplateCreationInfo]:
        template_creation_infos = self._gen_template_creation_infos()
        return self._sample_template_creation_infos(template_creation_infos)

    def _gen_template_creation_infos(self) -> list[TemplateCreationInfo]:
        data = []
        for template_file_path in self._get_all_template_file_paths():
            template_data = self._data_loader.load_json_data(
                template_file_path)
            data.append(TemplateCreationInfo(
                self._template_type, self._num_instances, template_data))
        return data
