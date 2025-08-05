from pylatex.base_classes import Environment
from pylatex.package import Package

class Multicols(Environment):

    packages = [Package("multicol")]
    escape = False
    content_separator = "\n"
    _latex_name = "multicols*"
