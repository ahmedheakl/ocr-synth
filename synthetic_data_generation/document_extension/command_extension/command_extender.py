from pylatex import Command, Document, NoEscape, UnsafeCommand

from .commands.document_write_position_log_command import DocumentWritePositionLogCommand
from .commands.log_paragraph_word_position_command import LogParagraphWordPositionCommand
from .commands.log_table_row_position_command import LogTableRowPositionCommand

class CommandExtender:

    def add_column_sep_command(self, doc: Document, col_sep: float):
        doc.preamble.append(UnsafeCommand(
            "setlength", [NoEscape("\columnsep"), f"{col_sep}pt"]))

    def add_base_commands(self, doc: Document):
        self.add_underscore_split_command(doc)
        self.add_url_prettifier_command(doc)
        self.add_write_position_log_commands(doc)

    def add_underscore_split_command(self, doc: Document):
        doc.preamble.append(Command("let\\underscore\\_"))
        command = Command(
            "discretionary",
            arguments=[NoEscape("\\underscore"), "", NoEscape("\\underscore")])
        doc.preamble.append(Command("renewcommand", arguments=["_", command]))

    def add_url_prettifier_command(self, doc: Document):
        doc.append(Command("sloppy"))

    def add_write_position_log_commands(self, doc: Document):
        self._add_main_text_item_commands(doc)
        self._add_paragraph_commands(doc)
        self._add_table_commands(doc)
        doc.preamble.append(
            UnsafeCommand(
                "newcommand",
                NoEscape(r"\lognewline"),
                options=2,
                extra_arguments=NoEscape(r"""
        \\%
        \zsavepos{#2}%
        \label{#2}%
        \write\mywrite{#1:\zposx{#2},\zposy{#2},\getpagerefnumber{#2}}%
        \RTL%
        """)
            )
        )
    def _add_main_text_item_commands(self, doc):
        self._add_new_main_text_item_write(doc)
        self._add_main_text_item_write_position_log_command(doc)

    def _add_new_main_text_item_write(self, doc: Document):
        doc.preamble.append(UnsafeCommand(
            "newcommand",
            NoEscape(
                f"\{DocumentWritePositionLogCommand().get_latex_name()}"),
            options=2,
            extra_arguments=(NoEscape(
                "\zsavepos{#1} \label{#2} "
                "\write\mywrite{#1:\zposx{#1},\zposy{#1},"
                "\getpagerefnumber{#2}}"))))

    def _add_main_text_item_write_position_log_command(self, doc: Document):
        doc.preamble.append(UnsafeCommand(
            "newwrite\\mywrite\n\\openout\\noexpand\\mywrite="
            "\\jobname.pos\\relax"))

    def _add_paragraph_commands(self, doc):
        self._add_new_paragraph_word_write(doc)
        self._add_paragraph_word_write_position_log_command(doc)

    def _add_new_paragraph_word_write(self, doc: Document):
        doc.preamble.append(UnsafeCommand(
            "newwrite\\paragraphwordwrite\n"
            "\\openout\\noexpand\\paragraphwordwrite=\\jobname.pwpos\\relax"))

    def _add_paragraph_word_write_position_log_command(self, doc: Document):
        doc.preamble.append(UnsafeCommand(
            "newcommand",
            NoEscape(f"\{LogParagraphWordPositionCommand().get_latex_name()}"),
            options=3,
            extra_arguments=NoEscape(
                r"{\begingroup"
                r"\raggedright"
                r"\label{#2} \zsavepos{#2} \write\paragraphwordwrite{"
                r"#1,,\arabic{page},,\zposx{#2},,\zposy{#2},,#3}"
                r"\endgroup}"
            )
        ))
    def _add_table_commands(self, doc: Document):
        self._add_table_row_commands(doc)

    def _add_table_row_commands(self, doc: Document):
        self._add_new_table_row_write(doc)
        self._add_table_row_write_position_log_command(doc)

    def _add_new_table_row_write(self, doc: Document):
        doc.preamble.append(UnsafeCommand(
            "newwrite\\tablerowwrite\n"
            "\\openout\\noexpand\\tablerowwrite=\\jobname.trpos"
            "\\relax"))

    def _add_table_row_write_position_log_command(self, doc: Document):
        doc.preamble.append(UnsafeCommand(
            "newcommand",
            NoEscape(f"\{LogTableRowPositionCommand().get_latex_name()}"),
            options=3,
            extra_arguments=(NoEscape(
                "\label{#3} \zsavepos{#3} \write\\tablerowwrite{"
                "#1,,\getpagerefnumber{#3},,#2,,\zposx{#3},,\zposy{#3}}"))))
