from pylatex.base_classes import Environment
from pylatex.package import Package
from pylatex import NoEscape

class TwoThirdsEnv(Environment):

    packages = [NoEscape("\\usepackage[\ntop=3cm,\nbottom=3cm,\nleft=2cm,\nright=7.25cm,\nmarginparwidth=4.25cm,\nmarginparsep=1cm,\nfootskip=1.5cm,\nheadsep=0.8cm,\nheadheight=1cm,\n]{geometry}")]

    escape = False
    content_separator = "\n"
    _latex_name = "twothirdswidth*"