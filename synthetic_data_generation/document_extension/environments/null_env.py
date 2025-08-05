from pylatex.base_classes import Environment

class NullEnv(Environment):
    """
    Environment that does nothing.
    """

    _latex_name = "nullenv"

    def __init__(self):
        super().__init__()
