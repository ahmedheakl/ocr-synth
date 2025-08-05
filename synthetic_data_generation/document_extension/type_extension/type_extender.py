from pylatex import Document, NoEscape, UnsafeCommand
from synthetic_data_generation.document_extension.type_extension.types.fixed_col_width_left_align_type import FixedColWidthLeftAlignType
from synthetic_data_generation.document_extension.type_extension.types.flexible_col_width_left_align_type import FlexibleColWidthLeftAlignType
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.templates.available_options.available_items import AvailableItems

class TypeExtender:

    type_initializer = "newcolumntype"

    def add_base_types(self, doc: Document):
        active_items = Template().get_active_items()
        if (active_items.has_item(AvailableItems.TABLE)):
            self.add_table_types(doc)

    def add_table_types(self, doc: Document):
        self._add_fixed_col_width_left_align_type(doc)
        self._add_flexible_col_width_left_align_type(doc)

    def _add_fixed_col_width_left_align_type(self, doc: Document):
        doc.preamble.append(
            UnsafeCommand(
                TypeExtender.type_initializer,
                FixedColWidthLeftAlignType._latex_name,
                options=1,
                extra_arguments=(NoEscape(">{\\arraybackslash}m{#1}"))))

    def _add_flexible_col_width_left_align_type(self, doc: Document):
        doc.preamble.append(
            UnsafeCommand(
                TypeExtender.type_initializer,
                FlexibleColWidthLeftAlignType._latex_name,
                options=1,
                extra_arguments=(
                    NoEscape(">{\\begin{varwidth}[m]{#1}}l<{\\end{varwidth}}"))
            )
        )
