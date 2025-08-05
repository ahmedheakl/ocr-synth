from synthetic_data_generation.document_extension.environments.table_environments.table_base_env import TableBaseEnv
from synthetic_data_generation.templates.util.style_item import StyleItem

class MulticolsOneColTableEnv(TableBaseEnv):

    def __init__(self, style: StyleItem):
        super().__init__(style)
