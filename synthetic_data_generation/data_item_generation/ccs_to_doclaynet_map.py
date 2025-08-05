from util.latex_item_type_names import LatexItemTypeNames

_map = {
    LatexItemTypeNames.CAPTION: "caption",
    LatexItemTypeNames.CHECKBOX_SELECTED: "checkbox_selected",
    LatexItemTypeNames.CHECKBOX_UNSELECTED: "checkbox_unselected",
    LatexItemTypeNames.CODE: "code",
    LatexItemTypeNames.FIGURE: "picture",
    LatexItemTypeNames.FOOTNOTE: "footnote",
    LatexItemTypeNames.FORMULA: "formula",
    LatexItemTypeNames.LINE_NUM: "line_number",
    LatexItemTypeNames.LIST_ITEM: "list_item",
    LatexItemTypeNames.PAGE_FOOTER: "page_footer",
    LatexItemTypeNames.PAGE_HEADER: "page_header",
    LatexItemTypeNames.PARAGRAPH: "paragraph",
    # LatexItemTypeNames.PICTURE: "picture",
    LatexItemTypeNames.REFERENCE: "text",
    LatexItemTypeNames.SECTION: "section_header",
    # LatexItemTypeNames.SUBSECTION: "?",
    # LatexItemTypeNames.SUBSUBSECTION: "?",
    LatexItemTypeNames.TABLE: "table",
    LatexItemTypeNames.TABLE_OF_CONTENTS: "document_index",
    LatexItemTypeNames.TEXT: "text",
    LatexItemTypeNames.TITLE: "title",
}

def ccs_to_doclay_net_type(item_type: str) -> str:
    if (item_type in _map):
        return _map[item_type]
    return None
