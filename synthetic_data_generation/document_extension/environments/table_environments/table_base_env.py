from synthetic_data_generation.document_extension.environments.base_env import BaseEnv
from synthetic_data_generation.templates.util.style_item import StyleItem

class TableBaseEnv(BaseEnv):

    _latex_name = "tablebase"

    def __init__(self, style: StyleItem, options=None, arguments=None):
        super().__init__(style, options=options, arguments=arguments)
