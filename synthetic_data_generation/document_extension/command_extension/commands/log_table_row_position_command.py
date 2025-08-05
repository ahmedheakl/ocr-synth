from pylatex.base_classes import CommandBase

class LogTableRowPositionCommand(CommandBase):

    _latex_name = "logTableRowPosition"

    def get_latex_name(self) -> str:
        return self._latex_name
