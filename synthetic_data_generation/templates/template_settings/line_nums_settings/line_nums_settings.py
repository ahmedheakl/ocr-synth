from synthetic_data_generation.templates.template_settings.layout_settings.layout_settings import LayoutSettings
from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner

class LineNumsSettings:

    def __init__(self, template: dict, layout_settings: LayoutSettings):
        line_nums_config = TemplateQuestioner(template).get_line_nums_config()
        self._are_displayed = self._resolve_are_displayed(
            line_nums_config, layout_settings)
        self._are_in_ro = (self._resolve_are_in_ro(line_nums_config) if
            (self._are_displayed) else False)

    def are_displayed(self) -> bool:
        return self._are_displayed

    def are_in_ro(self) -> bool:
        return self._are_in_ro

    def _resolve_are_displayed(
        self, line_nums_config: dict, layout_settings: LayoutSettings
    ) -> bool:
        if (layout_settings.get_num_cols() > 2):
            return False
        if (TemplateKeys.ARE_DISPLAYED in line_nums_config):
            are_displayed = line_nums_config[TemplateKeys.ARE_DISPLAYED]
            if (type(are_displayed) == bool):
                return are_displayed
        return False

    def _resolve_are_in_ro(self, line_nums_config: dict) -> bool:
        if (TemplateKeys.ARE_INCLUDED_IN_RO in line_nums_config):
            are_in_ro = line_nums_config[TemplateKeys.ARE_INCLUDED_IN_RO]
            if (type(are_in_ro) == bool):
                return are_in_ro
        return False
