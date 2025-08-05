from synthetic_data_generation.serializer import data_to_latex_type_serializer as serializer
from synthetic_data_generation.document_extension.command_extension.commands.log_paragraph_word_position_command import LogParagraphWordPositionCommand
from .text_item import TextItem
from pylatex import Document, NewLine, NoEscape, Command
from pylatex import Figure, Section, Subsection, Subsubsection, Table
import time
from synthetic_data_generation.data_item_generation.data_items.util.lang import is_latin_text, _wrap_latin_segments, wrap_latin_segments, escape_everything_except_eng, clean_latin_in_eng_tag
from pylatex.utils import escape_latex

class SectionItem(TextItem):

    def __init__(self, index, data: dict):
        super().__init__(index, data)

    def add_as_latex_to_doc(self, doc):
        doc.log_write_position(self._index)
        self._create_section(doc)
        doc.log_write_position(self._index)

    def _create_section(self, doc):
        # ➊ log position …
        log_cmd = f"\\{LogParagraphWordPositionCommand().get_latex_name()}{{{self._index}}}{{palabel{self._index}}}{{ }}"
        doc.append(NoEscape("%"))
        doc.append(NoEscape(log_cmd))

        section_cls = serializer.data_to_latex_type(self._type)

        # ➋ wrap first
        wrapped_text = _wrap_latin_segments(self._text)
        escaped_text = escape_everything_except_eng(wrapped_text)
        render_text = self._split_long_unbreakable_char_sequences(escaped_text)
        render_text = clean_latin_in_eng_tag(render_text)
        section_instance = Section(NoEscape(render_text))
        doc.append(section_instance)