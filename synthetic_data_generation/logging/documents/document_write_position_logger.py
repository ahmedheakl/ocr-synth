from pylatex.base_classes import Arguments

from ...document_extension.command_extension.commands.document_write_position_log_command import DocumentWritePositionLogCommand

class DocumentWritePositionLogger:

    def __init__(self):
        self._is_start_position = True

    def log_position(self, doc, item_index):
        doc.append(DocumentWritePositionLogCommand(
            arguments=self._create_args(item_index)))
        self._is_start_position = not self._is_start_position

    def _create_args(self, item_index):
        return Arguments(
            self._get_pos_identifier_arg(item_index),
            self._get_page_identifier_arg(item_index))

    def _get_pos_identifier_arg(self, item_index):
        if (self._is_start_position):
            return f"spos{item_index}"
        return f"epos{item_index}"

    def _get_page_identifier_arg(self, item_index):
        if (self._is_start_position):
            return f"spage{item_index}"
        return f"epage{item_index}"
