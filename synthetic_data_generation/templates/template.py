from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.template_settings.active_items import ActiveItems
from synthetic_data_generation.templates.template_settings.figure_item_settings.figure_item_settings import FigureItemSettings
from synthetic_data_generation.templates.template_settings.layout_settings.layout_settings import LayoutSettings
from synthetic_data_generation.templates.template_settings.table_item_settings.table_item_settings import TableItemSettings
from synthetic_data_generation.templates.template_settings.text_item_settings.text_item_settings import TextItemSettings
from synthetic_data_generation.templates.template_settings.excluded_reading_order_items import ExcludedReadingOrderItems
from synthetic_data_generation.templates.template_settings.line_nums_settings.line_nums_settings import LineNumsSettings
from synthetic_data_generation.templates.template_settings.list_items_settings.list_items_settings import ListItemsSettings
from synthetic_data_generation.templates.template_settings.watermark_settings.watermark_settings import WatermarkSettings

class Template:
    """
    Holds all information about the template currently in use to generate
    latex documents from it.
    """

    _instance = None
    _unnamed_template_cnt = 0

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(Template, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True

    def get_name(self) -> str:
        return self._name

    def get_layout_settings(self) -> LayoutSettings:
        return self._template_layout_settings

    def get_active_items(self) -> ActiveItems:
        return self._active_items

    def get_excluded_reading_order_items(self) -> ExcludedReadingOrderItems:
        return self._excluded_ro_items

    def get_figure_item_settings(self) -> FigureItemSettings:
        return self._figure_item_settings

    def get_table_item_settings(self) -> TableItemSettings:
        return self._table_item_settings

    def get_text_item_settings(self) -> TextItemSettings:
        return self._text_item_settings

    def get_watermark_settings(self) -> WatermarkSettings:
        return self._watermark_settings

    def get_line_nums_settings(self) -> LineNumsSettings:
        return self._line_nums_settings

    def get_list_items_settings(self) -> ListItemsSettings:
        return self._list_items_settings

    def is_configured(self) -> bool:
        return ((self._initialized) and (self._name != ""))

    def configure(self, template: dict):
        try:
            self._configure(template)
        except Exception as e:
            self.clear()
            raise e

    def clear(self):
        self._name = ""
        self._template_layout_settings = None
        self._active_items = None
        self._excluded_ro_items = None
        self._figure_item_settings = None
        self._table_item_settings = None
        self._text_item_settings = None
        self._watermark_settings = None
        self._line_nums_settings = None
        self._list_items_settings = None

    def _configure(self, template: dict):
        self._name = self._resolve_template_name(template)
        self._template_layout_settings = LayoutSettings(template)
        self._active_items = ActiveItems(template)
        self._excluded_ro_items = ExcludedReadingOrderItems(template)
        self._figure_item_settings = FigureItemSettings(
            template, self._template_layout_settings.get_num_cols())
        self._table_item_settings = TableItemSettings(
            template, self._template_layout_settings.get_num_cols())
        self._text_item_settings = TextItemSettings(template)
        self._watermark_settings = WatermarkSettings(template)
        self._line_nums_settings = LineNumsSettings(
            template, self._template_layout_settings)
        self._list_items_settings = ListItemsSettings(template)

    def _resolve_template_name(self, template: dict) -> str:
        if ((TemplateKeys.TEMPLATE_NAME in template) and
            (type(template[TemplateKeys.TEMPLATE_NAME]) == str)):
            return template[TemplateKeys.TEMPLATE_NAME]
        template_name = f"unnamed_template_{Template._unnamed_template_cnt}"
        Template._unnamed_template_cnt += 1
        return template_name
