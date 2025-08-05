from synthetic_data_generation.templates.util.template_keys import TemplateKeys

class TemplateCreationInfo:

    def __init__(
        self, template_type: str, num_instances: int, template_data: dict
    ):
        self._template_type = template_type
        self._template_name = template_data[TemplateKeys.TEMPLATE_NAME]
        self._num_instances = num_instances
        self._template_data = template_data

    def get_template_type(self) -> str:
        return self._template_type

    def get_template_name(self) -> str:
        return self._template_name

    def get_num_instances(self) -> int:
        return self._num_instances

    def get_template_data(self) -> dict:
        return self._template_data
