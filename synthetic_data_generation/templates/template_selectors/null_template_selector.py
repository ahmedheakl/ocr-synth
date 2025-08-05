from .template_creation_info import TemplateCreationInfo
from .template_selector import TemplateSelector

class NullTemplateSelector(TemplateSelector):

    def __init__(self, *args, **kwargs):
        pass

    def select_template_creation_infos(self) -> list[TemplateCreationInfo]:
        return []
