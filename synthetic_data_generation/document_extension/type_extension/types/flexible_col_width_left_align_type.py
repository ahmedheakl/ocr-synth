from pylatex.base_classes import CommandBase
from pylatex.package import Package

class FlexibleColWidthLeftAlignType(CommandBase):

    _latex_name = "U"
    packages = [
        Package("varwidth")
    ]
