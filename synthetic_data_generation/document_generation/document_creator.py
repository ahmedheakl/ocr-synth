import logging
import random
import re

from pylatex import Command
from pylatex.utils import NoEscape
from synthetic_data_generation.data_item_generation import data_item_map
from synthetic_data_generation.data_stores.main_text_item_store import MainTextItemStore
from synthetic_data_generation.data_item_generation.data_items.figure_item.figure_item import FigureItem
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.data_structures.latex_document.custom_document import CustomDocument
from synthetic_data_generation.document_extension.command_extension.command_extender import CommandExtender
from synthetic_data_generation.document_extension.environments.landscape_env import LandscapeEnv
from synthetic_data_generation.document_extension.environments.multicols_env import Multicols
from synthetic_data_generation.document_extension.environments.null_env import NullEnv
from util.data_stores.docling_data_store import DoclingDataStore
from util.latex_item_type_names import LatexItemTypeNames
from util.retrieve_index_from_reference import (
    retrieve_component_from_index_and_type,
    retrieve_index_type_from_reference_string
)

logger = logging.getLogger(__name__)

HSP_L = r"\hspace{0.5em}"
HSP_R = r"\hspace{0.5em}"
MATH_PATTERN = re.compile(r'\\\(.*?\\\)')

def fix_latex_math(text):
    if not isinstance(text, str):
        return text

    def replacer(match):
        math_expr = match.group(0)
        corrected_expr = math_expr.replace("\\\\", "\\")
        if corrected_expr != math_expr:
            logger.debug(f"Fixed LaTeX math: {math_expr} -> {corrected_expr}")
        return corrected_expr

    return MATH_PATTERN.sub(replacer, text)

class DocumentCreator:
    def __init__(self):
        self._main_text = DoclingDataStore().get_main_text()
        self._active_items = Template().get_active_items()
        self._list_items_settings = Template().get_list_items_settings()
        self._chart_generation_flag = Template().get_layout_settings().is_gen_chart()
        logger.info("DocumentCreator initialized")

    def create_doc(self):
        logger.info("Creating document")
        doc = CustomDocument("doc")
        self._write_content(doc)
        return doc

    def _write_content(self, doc: CustomDocument):
        with doc.create(self._create_page_format_env()):
            with doc.create(self._create_page_col_env(doc)):
                self._add_items_to_doc(doc)

    def _create_page_format_env(self):
        layout_settings = Template().get_layout_settings()
        return LandscapeEnv() if layout_settings.is_page_format_landscape() else NullEnv()

    def _create_page_col_env(self, doc: CustomDocument):
        layout_settings = Template().get_layout_settings()
        if layout_settings.has_one_col():
            return NullEnv()
        CommandExtender().add_column_sep_command(doc, layout_settings.get_col_sep_pt())
        return Multicols(arguments=str(layout_settings.get_num_cols()))

    def _add_items_to_doc(self, doc: CustomDocument):
        main_text_item_store = MainTextItemStore()
        item_index = 0
        try:
            for item in self._main_text:
                print(f"[DEBUG] Processing item index {item_index}: {item}")
                if self._is_table_item(item):
                    item_instance = data_item_map.data_to_instance(item_index, item)
                    print(f"[DEBUG] Created instance: {item_instance}")
                    self._add_table_item_to_doc(item_index, item, doc, main_text_item_store)
                    item_index += 2 if self._has_caption(item) else 1

                elif self._is_list_item(item):
                    count = self._add_list_items_to_doc(item_index, item, doc, main_text_item_store)
                    item_index += count

                elif self._is_picture_item(item):
                    item_instance = data_item_map.data_to_instance(item_index, item)
                    main_text_item_store.add_item(item_instance)
                    item_instance.add_as_latex_to_doc(doc, main_text_item_store)
                    item_index += 2 if self._has_caption(item) else 1
                else:
                    item_instance = data_item_map.data_to_instance(item_index, item)
                    print(f"[DEBUG] Adding item {item_index} to LaTeX: {getattr(item_instance, '_value', '')}")
                    if item_instance.is_valid() and not item_instance.is_caption():
                        item_instance.add_as_latex_to_doc(doc)
                        main_text_item_store.add_item(item_instance)
                        item_index += 1
        except Exception as e:
            print("skipped item: 🚨", item)
            print(e)
            print("------------------------------------------")

    def _add_list_items_to_doc(self, item_index, item, doc, main_text_item_store):
        with doc.create(self._list_items_settings.gen_env()) as itemize:
            components = item.get('children', [])
            processed = 0
            for comp in components:
                comp_ref = comp['$ref']
                index, type_str = retrieve_index_type_from_reference_string(comp_ref)
                subitem = retrieve_component_from_index_and_type(index, type_str)
                item_instance = data_item_map.data_to_instance(item_index + processed, subitem)
                main_text_item_store.add_item(item_instance)
                itemize.append(Command("item"))
                item_instance.add_as_latex_to_doc(doc)
                processed += 1
        return processed

    def _add_table_item_to_doc(self, item_index, item, doc, main_text_item_store):
        item_instance = data_item_map.data_to_instance(item_index, item)
        if item_instance.is_valid():
            item_instance.add_as_latex_to_doc(doc, main_text_item_store)

    def _add_caption_to_doc_items(self, item, main_text_item_store, item_index, doc):
        captions = item.get('captions', [])
        if captions:
            ref = captions[0]['$ref'].split('/')
            caption_index = int(ref[2])
            caption_data = DoclingDataStore().get_text_by_index(caption_index)
            caption_instance = data_item_map.data_to_instance(item_index, caption_data)
            caption_instance.add_as_latex_to_doc(doc)
            main_text_item_store.add_item(caption_instance)
        return len(captions)

    def _add_generated_chart_to_doc(self, item_index, item, doc, main_text_item_store, parent):
        chart_item = FigureItem.from_table(item, parent)
        if chart_item is None:
            return 1
        chart_item = chart_item.dict()
        item_instance = data_item_map.data_to_instance(item_index, chart_item)
        main_text_item_store.add_item(item_instance)
        item_instance.add_as_latex_to_doc(doc, main_text_item_store)
        return 1

    def _add_inline_items_to_doc(watlf, item_index, item, doc, main_text_item_store):
        components = item.get('children', [])
        processed = 0
        for comp in components:
            index, type_str = retrieve_index_type_from_reference_string(comp['$ref'])
            subitem = retrieve_component_from_index_and_type(index, type_str)
            if 'formula' in subitem.get('label', ''):
                subitem['label'] = 'inline'
            item_instance = data_item_map.data_to_instance(item_index + processed, subitem)
            main_text_item_store.add_item(item_instance)
            item_instance.add_as_latex_to_doc(doc)
            processed += 1
        return processed

    def _is_list_item(self, item):
        return item.get("label") in {"list", "ordered_list"}

    def _is_picture_item(self, item):
        return item.get("label") == LatexItemTypeNames.FIGURE

    def _is_inline_item(self, item):
        return item.get("label") == LatexItemTypeNames.INLINE

    def _is_table_item(self, item):
        return item.get("label") == LatexItemTypeNames.TABLE

    def _has_caption(self, item):
        return bool(item.get('captions'))