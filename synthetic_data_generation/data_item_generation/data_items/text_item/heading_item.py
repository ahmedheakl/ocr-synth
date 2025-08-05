from pylatex import NewLine, Package

from synthetic_data_generation.data_structures.latex_document.page_heading import PageHeading
from synthetic_data_generation.document_extension.command_extension.commands.font_commands_creator import FontCommandsCreator
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.templates.template_settings.layout_settings.layout_settings import LayoutSettings
from util.retrieve_index_from_reference import retrieve_index_from_reference
from .text_item import TextItem

class HeadingItem(TextItem):

    def __init__(self, index, data: dict):
        super().__init__(index, data)
        self._page_num = data["prov"][0]["page_no"]

    def _write_content_to_heading(self, page_heading: PageHeading, env, doc):
        page_style = page_heading.get_page_style()
        header_items = page_heading.get_header_items()
        with page_style.create(env) as heading_env:
            self._set_style(heading_env)
            self._write_existing_content_to_heading(heading_env, header_items)
            self._write_new_content_to_heading(heading_env, doc)

    def _set_style(self, heading_env):
        layout_settings = Template().get_layout_settings()
        self._set_font_color(heading_env, layout_settings)
        self._set_font_size(heading_env, layout_settings)
        self._set_font_style(heading_env, layout_settings)

    def _set_font_color(self, heading_env, layout_settings: LayoutSettings):
        color = layout_settings.get_font_color()
        heading_env.append(FontCommandsCreator.create_color_command(color))

    def _set_font_size(self, heading_env, layout_settings: LayoutSettings):
        size = layout_settings.get_font_size_as_latex_str()
        heading_env.append(FontCommandsCreator.create_size_command(size))

    def _set_font_style(self, heading_env, layout_settings: LayoutSettings):
        font_style = layout_settings.get_font_style()
        font_family = font_style.get_latex_code()
        packages = [Package(font_style.get_latex_package_name())]
        heading_env.append(FontCommandsCreator.create_style_command(
            font_family, packages))
        heading_env.append(FontCommandsCreator.create_select_font_command())

    def _write_existing_content_to_heading(self, heading_env, items: list):
        for item in items:
            for text_line in item.get_text_lines():
                heading_env.append(text_line)
                heading_env.append(NewLine())

    def _write_new_content_to_heading(self, heading_env, doc):
        excluded_ro_items = Template().get_excluded_reading_order_items()
        is_in_reading_order = not excluded_ro_items.has_item(self._type)
        if (is_in_reading_order):
            doc.log_write_position(self._index)
        heading_env.append(self._text)
        heading_env.append(NewLine())
        if (is_in_reading_order):
            doc.log_write_position(self._index)

    def _has_reference(self, data: dict) -> bool:
        ref_index = retrieve_index_from_reference(data)
        return (ref_index is not None)
