from pylatex.base_classes import Environment
from pylatex.package import Package

class LandscapeEnv(Environment):

    packages = [Package("lscape")]
    escape = False
    content_separator = "*\n"

    _latex_name = "landscape"
