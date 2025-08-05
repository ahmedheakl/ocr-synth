from pylatex.base_classes import CommandBase

class LogParagraphWordPositionCommand(CommandBase):

    _latex_name = "logParagraphWordPosition"

    def get_latex_name(self) -> str:
        return self._latex_name
