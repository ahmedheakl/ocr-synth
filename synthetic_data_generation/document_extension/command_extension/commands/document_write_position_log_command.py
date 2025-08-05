from pylatex import NoEscape
from pylatex.base_classes import CommandBase
from pylatex.package import Package

class DocumentWritePositionLogCommand(CommandBase):

    _latex_name = "documentWritePositionLogCommand"
    packages = [
        Package("geometry"),
        Package("refcount"),
        Package(NoEscape("zref-savepos")),
        Package(NoEscape("zref-user"))
    ]

    def get_latex_name(self) -> str:
        return self._latex_name
