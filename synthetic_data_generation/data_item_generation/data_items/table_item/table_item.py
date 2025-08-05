from pylatex import NewLine, NewPage, VerticalSpace, Command, NoEscape

from synthetic_data_generation.data_item_generation.data_items.main_text_item import MainTextItem
from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.data_stores.wrap_items_store import WrapItemsStore
from synthetic_data_generation.data_stores.wrap_item_store_item import WrapItemStoreItem
from synthetic_data_generation.document_extension.environments.landscape_env import LandscapeEnv
from synthetic_data_generation.document_extension.environments.table_environments.wraptable_env import WraptableEnv
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.items_position_stores_manager import ItemsPositionStoresManager
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.stores.table.table_item_positions import TableItemPositions
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.stores.table.table_item_row_position import TableItemRowPosition
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_data import GroundTruthData

from synthetic_data_generation.templates.template import Template
from util import bbox_service
from util.latex_item_type_names import LatexItemTypeNames
from .table_row import TableRow
from .table_segment_data import TableSegmentData
from docling_core.types.doc.document import TableData, TableCell
from pylatex import Table, Tabular, MultiColumn, MultiRow
from pylatex.utils import NoEscape, escape_latex
from util.retrieve_index_from_reference import retrieve_component_from_index_and_type, retrieve_index_type_from_reference_string
from synthetic_data_generation.data_item_generation import data_item_map
from pylatex import NewLine, NewPage, VerticalSpace, Command, NoEscape
import logging

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import re
import random

HSP_L = r"\hspace{0.5em}"   # left  pad
HSP_R = r"\hspace{0.5em}"   # right pad

MATH_PATTERN = re.compile(r'\\\(.*?\\\)')

def fix_latex_math(text):
    """Finds LaTeX math in \( ... \) and ensures correct escaping inside."""
    if not isinstance(text, str):
        return text  # Only process strings

    def replacer(match):
        math_expr = match.group(0)
        corrected_expr = math_expr.replace("\\\\", "\\")
        if corrected_expr != math_expr:
            logger.debug(f"Fixed LaTeX: {math_expr} -> {corrected_expr}")
        return corrected_expr

    return MATH_PATTERN.sub(replacer, text)


class TableItem(MainTextItem):

    _max_cols_portrait_page = 15
    _max_cols_landscape_page = 20
    _max_row_before_changing_page = 8

    def __init__(self, index, data: dict):
        for i, prov in enumerate(data.get("prov", [])):
            data["prov"][i]["charspan"] = (0, 0)

        super().__init__(index, data)

        table_item_data = self._get_table_data(data)
        self._table_data_dict = table_item_data

        self._num_rows = table_item_data["num_rows"]
        self._num_cols = table_item_data["num_cols"]
        self._table_rows = self._gen_table_rows(index, table_item_data)
        self.caption = data['captions']

        self.data = TableData(
            num_rows=self._num_rows,
            num_cols=self._num_cols,
            table_cells=self._table_data_dict["table_cells"]
        )
        self._self_ref = data.get("self_ref", f"#/tables/{index}")
        logger.debug(f"Initialized TableItem with shape {self._num_rows}x{self._num_cols}")

    def is_valid(self) -> bool:
        return self._num_rows > 0 and self._num_cols > 0

    def get_table_data_dict(self):
        return self._table_data_dict

    def get_table_rows(self):
        return self._table_rows

    def get_num_rows(self):
        return self._num_rows

    def get_num_cols(self):
        return self._num_cols

    def get_segment_data(
        self,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> list[dict]:
        table_segment_data = self._gen_table_segment_data(
            prov_item, pos_stores_manager)
        return [table_segment_data.to_dict()]

    def has_text_break(
        self,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> bool:
        table_segment_data = self._gen_table_segment_data(
            prov_item, pos_stores_manager)
        return table_segment_data.has_text_break()

    def has_page_break(
        self,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> bool:
        table_segment_data = self._gen_table_segment_data(
            prov_item, pos_stores_manager)
        return table_segment_data.has_page_break()

    def _gen_table_segment_data(
        self,
        prov_item: ProvItem,
        pos_stores_manager: ItemsPositionStoresManager
    ) -> TableSegmentData:
        table_pos_store = pos_stores_manager.get_table_positions_store()
        positions = table_pos_store.get_item_positions(self._index)
        row_positions = positions.get_row_positions_of_page(
            prov_item.get_page_num())
        segment_data = TableSegmentData()
        for row_position in row_positions:
            self._add_row(segment_data, prov_item, row_position)
        self._set_break_tag(segment_data, prov_item, positions)
        return segment_data

    def _add_row(
        self,
        segment_data: TableSegmentData,
        prov_item: ProvItem,
        row_position: TableItemRowPosition
    ):
        (left, top) = row_position.get_position()
        if (bbox_service.is_point_in_bbox(left, top, prov_item.get_bbox())):
            row = self._table_rows[row_position.get_row_index()]
            segment_data.add_html(row.to_html())
            segment_data.add_otsl(row.to_otsl())

    def _set_break_tag(
        self,
        segment_data: TableSegmentData,
        prov_item: ProvItem,
        positions: TableItemPositions
    ):
        if self._continues_on_this_page(prov_item, positions):
            segment_data.set_text_break()
        elif (self._continues_on_other_page(prov_item, positions)):
            segment_data.set_page_break()

    def _continues_on_this_page(
        self, prov_item: ProvItem, positions: TableItemPositions
    ) -> bool:
        page_num = prov_item.get_page_num()
        last_row_position = positions.get_last_row_of_page(page_num)
        (left, top) = last_row_position.get_position()
        bbox = prov_item.get_bbox()
        return not (bbox_service.is_point_in_bbox(left, top, bbox))

    def _continues_on_other_page(
        self, prov_item: ProvItem, positions: TableItemPositions
    ) -> bool:
        return (prov_item.get_page_num() < positions.get_page_num_last())


    def _has_active_caption(self) -> bool:
        return bool(self.caption)

    def _get_caption_item_index(self):
        caption_ref = self.caption[0]["$ref"]
        return retrieve_index_type_from_reference_string(caption_ref)

    def _get_caption_document_index(self):
        # caption is always the element after the table item
        return self._index + 1

    def _add_table_caption_to_doc(self, table_env, doc, main_text_item_store):
        if not self._has_active_caption():
            doc.append(NewLine())
            return

        cap_idx, cap_type = self._get_caption_item_index()
        caption_node = retrieve_component_from_index_and_type(cap_idx, cap_type)

        item_instance = data_item_map.data_to_instance(self._index + 1, caption_node)
        item_instance.set_caption()

        GroundTruthData().add_with_overwrite_existing_item(item_instance)

        doc.log_write_position(self._get_caption_document_index())

        latex_caption_text = item_instance.get_latex_text()
        table_env.add_caption(NoEscape(latex_caption_text))

        main_text_item_store.add_item(item_instance)
        doc.log_write_position(self._get_caption_document_index())


    def add_as_latex_to_doc(self, doc, main_text_item_store):
        """
        Render the table as LaTeX, taking care of both RTL (Arabic) and LTR layouts.
        """
        # --- 0.  Boiler-plate ----------------------------------------------------
        layout_settings = Template().get_layout_settings()
        is_rtl         = layout_settings.is_arabic()     # -> True for Arabic, False otherwise
        doc.log_write_position(self._index)

        td: TableData = self.data
        n_rows, n_cols = td.num_rows, td.num_cols
        cells = td.table_cells

        # --- 1.  Build a logical grid -------------------------------------------
        grid = [[None for _ in range(n_cols)] for _ in range(n_rows)]
        for cell in cells:
            r0, r1 = cell.start_row_offset_idx, cell.end_row_offset_idx
            c0, c1 = cell.start_col_offset_idx, cell.end_col_offset_idx
            rowspan, colspan = r1 - r0, c1 - c0
            grid[r0][c0] = (cell.text, rowspan, colspan)
            for r in range(r0, r1):
                for c in range(c0, c1):
                    if (r, c) != (r0, c0):
                        grid[r][c] = "SPAN"

        # --- 2.  Random styling decisions (unchanged) ----------------------------
        col_align  = random.choice(["l", "c", "r"])
        use_vlines = random.choice([True, False])
        use_booktab = random.choice([True, False])
        shade_rows = random.choice([True, False])
        shade_color = random.choice(["gray!15", "blue!10", "yellow!15", "green!10"])
        width_fact = round(random.uniform(0.6, 1.0), 2)

        col_spec_core = col_align * n_cols
        col_spec = ("|" if use_vlines else "") + "|".join(col_spec_core) + ("|" if use_vlines else "")

        def top_rule(t): t.add_hline() if not use_booktab else t.append(NoEscape(r"\toprule"))
        def mid_rule(t): t.add_hline() if not use_booktab else t.append(NoEscape(r"\midrule"))
        def bot_rule(t): t.add_hline() if not use_booktab else t.append(NoEscape(r"\bottomrule"))

        def _cell_span(obj):
            if isinstance(obj, MultiColumn): return obj.size
            if isinstance(obj, MultiRow):    return _cell_span(obj.data)
            return 1

        # --- 3.  Helper for direction-dependent text -----------------------------
        def _wrap(txt: str) -> NoEscape:
            """
            Wrap cell text with \RL{...} for RTL, otherwise leave plain.
            """
            safe = escape_latex(fix_latex_math(txt))
            return NoEscape(rf"\RL{{{safe}}}") if is_rtl else NoEscape(safe)

        # --- 4.  Emit LaTeX -------------------------------------------------------
        with doc.create(Table(position="H")) as table_env:
            table_env.append(
                NoEscape(r"\resizebox{\textwidth}{!}{")
            )
            with table_env.create(Tabular(col_spec)) as tab:
                top_rule(tab)

                for r in range(n_rows):
                    # alternate shading

                    def _maybe_shade(txt_wrapped):
                        if shade_rows and r % 2 == 1:
                            return NoEscape(r"\cellcolor{%s} %s" % (shade_color, txt_wrapped))
                        return txt_wrapped
                    
                
                    row_cells, c = [], 0
                    while c < n_cols:
                        cell = grid[r][c]
                        if cell == "SPAN" or cell is None:
                            row_cells.append("")
                            c += 1
                            continue

                        txt, rowspan, colspan = cell
                        txt_wrapped = _maybe_shade(_wrap(txt))
                        if rowspan > 1 and colspan > 1:
                            obj = MultiRow(
                                rowspan,
                                data=MultiColumn(colspan,
                                                align=("|%s|" % col_align) if use_vlines else col_align,
                                                data=txt_wrapped))
                        elif rowspan > 1:
                            obj = MultiRow(rowspan, data=txt_wrapped)
                        elif colspan > 1:
                            obj = MultiColumn(colspan,
                                            align=("|%s|" % col_align) if use_vlines else col_align,
                                            data=txt_wrapped)
                        else:
                            obj = txt_wrapped
                        row_cells.append(obj)
                        c += colspan if colspan > 1 else 1

                    # Reverse only for RTL
                    if is_rtl:
                        row_cells = list(reversed(row_cells))

                    # Make sure the row has exactly n_cols cells
                    deficit = n_cols - sum(_cell_span(x) for x in row_cells)
                    if deficit > 0:
                        filler = [""] * deficit
                        row_cells = (row_cells + filler) if not is_rtl else (filler + row_cells)

                    tab.add_row(row_cells)

                    if not any(isinstance(grid[r][c], tuple) and grid[r][c][1] > 1 for c in range(n_cols)):
                        mid_rule(tab)

                bot_rule(tab)
            table_env.append(NoEscape("}"))

            # Spacing + position logs
            self._add_table_spacing(doc)
            doc.log_write_position(self._index)
            self._add_table_spacing(doc)

            # Caption (still works the same)
            self._add_table_caption_to_doc(table_env, doc, main_text_item_store)

        main_text_item_store.add_item(self)
    
    def _add_table_spacing(self, doc):
        # only needed in one-column layouts; matches figure behaviour
        if Template().get_layout_settings().has_one_col():
            doc.append(NewLine())

    def _has_data(self):
        return ((self._num_rows > 0) and (self._num_cols > 0))

    def _is_table_too_large(self):
        return (self._num_cols > TableItem._max_cols_landscape_page)

    def _append_table_to_doc(self, doc):
        table_item_settings = Template().get_table_item_settings()
        env = table_item_settings.get_table_env(self._num_rows, self._num_cols)
        if (self._is_wrapable_env(env)):
            self._append_wrap_table_to_doc(doc, env)
        else:
            self._append_regular_table_to_doc(doc, env)

    def _is_wrapable_env(self, env) -> bool:
        return (type(env) == WraptableEnv)

    def _append_wrap_table_to_doc(self, doc, env):
        self._store_item_data_to_wrapable_item_store(env)
        with doc.create(env):
            table = self._gen_table(env)
            self._append_table_to_doc_given_table_size(table, doc)

    def _append_regular_table_to_doc(self, doc, env):
        with doc.create(env):
            table = self._gen_table(env)
            self._append_table_to_doc_given_table_size(table, doc)

    def _gen_table(self, env):
        return None

    def _store_item_data_to_wrapable_item_store(self, env: WraptableEnv):
        store_item = WrapItemStoreItem(LatexItemTypeNames.TABLE, self._index,
            env.get_wrap_position(), env.get_line_width())
        WrapItemsStore().add_item(store_item)

    def _append_table_to_doc_given_table_size(self, table, doc):
        self._position_cursor_above_table(doc)
        doc.log_write_position(self._index)
        self._add_space_above_table_to_get_valid_bbox_top(doc)
        if (self._table_fits_on_portrait_page()):
            self._append_table_to_portrait_page(table, doc)
        else:
            self._append_table_to_landscape_page(table, doc)
        self._add_space_below_table_to_get_valid_bbox_top(doc)
        doc.log_write_position(self._index)
        self._move_items_below_table_down_by_one_line(doc)

    def _table_fits_on_portrait_page(self):
        return not (self._num_cols > TableItem._max_cols_portrait_page)

    def _append_table_to_portrait_page(self, table, doc):
        if self._num_rows > TableItem._max_row_before_changing_page:
            doc.append(NoEscape(r"\resizebox{\textwidth}{!}{"))
        doc.append(table)
        doc.append(NoEscape(r"}"))

    def _append_table_to_landscape_page(self, table, doc):
        doc.append(NewPage())
        with doc.create(LandscapeEnv()):
            doc.log_write_position(self._index)
            doc.append(table)
            self._add_space_below_table_to_get_valid_bbox_top(doc)
            doc.log_write_position(self._index)
        doc.append(NewPage())

    def _position_cursor_above_table(self, doc):
        doc.append(VerticalSpace("14px"))
        doc.append(NewLine())

    def _add_space_above_table_to_get_valid_bbox_top(self, doc):
        doc.append(NewLine())

    def _add_space_below_table_to_get_valid_bbox_top(self, doc):
        layout_settings = Template().get_layout_settings()
        baseline_skip = layout_settings.get_baseline_skip_px()
        doc.append(VerticalSpace(f"{baseline_skip}px"))
        doc.append(NewLine())

    def _move_items_below_table_down_by_one_line(self, doc):
        doc.append(NewLine())

    def _get_table_data(self, data: dict):
        data = data.get('data', {})
        table_cells = data['table_cells']
        new_table_cells = []
        for cell in table_cells:
            if cell['start_row_offset_idx'] == cell['end_row_offset_idx']:
                cell['end_row_offset_idx'] += 1
            if cell['start_col_offset_idx'] == cell['end_col_offset_idx']:
                cell['end_col_offset_idx'] += 1
            new_table_cells.append(cell)
        data['table_cells'] = new_table_cells
        return data

    def _gen_table_rows(
            self,
            table_item_index: int,
            table_item_data: dict
    ) -> list[TableRow]:
        """
        Build a full 2-D grid first (num_rows × num_cols) and then map every
        TableCell into that grid according to its start/end offsets.  Spanning
        cells are replicated in every covered slot so later code can simply
        iterate row-by-row.

        Returns
        -------
        list[TableRow]
            A TableRow for every logical row in the table.  The method never
            returns [] unless num_rows or num_cols is 0.
        """

        num_rows: int = table_item_data["num_rows"]
        num_cols: int = table_item_data["num_cols"]
        raw_cells: list[dict] = table_item_data["table_cells"]

        if num_rows == 0 or num_cols == 0:
            return []

        # 1.  allocate an empty grid
        grid: list[list[TableCell | None]] = [
            [None for _ in range(num_cols)] for _ in range(num_rows)
        ]

        # 2.  place every raw cell into the grid, expanding spans
        for cell_dict in raw_cells:
            cell = TableCell(**cell_dict)

            for r in range(cell.start_row_offset_idx, cell.end_row_offset_idx):
                for c in range(cell.start_col_offset_idx, cell.end_col_offset_idx):
                    if r >= num_rows or c >= num_cols:
                        raise ValueError(
                            f"Cell {cell.text!r} exceeds table bounds "
                            f"({num_rows}×{num_cols}) at ({r},{c})"
                        )
                    grid[r][c] = cell

        # 3.  convert each grid row into a TableRow
        rows: list[TableRow] = []
        for row_idx, row_cells in enumerate(grid):
            # Convert Nones (unfilled slots) into empty TableCells so that
            # downstream LaTeX code gets a placeholder instead of crashing.
            safe_cells = [
                TableCell(text="", start_row_offset_idx=0, end_row_offset_idx=1,
                    start_col_offset_idx=0, end_col_offset_idx=1) if cell is None else cell
                for cell in row_cells
            ]
            rows.append(
                TableRow(
                    table_item_index,
                    row_idx,
                    safe_cells,
                    num_cols,
                )
            )

        return rows