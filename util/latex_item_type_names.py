class LatexItemTypeNames:
    """
    This class stores all the item type names that are available in the
    ccs data format.
    """

    CAPTION = "caption"
    CHECKBOX_SELECTED = "checkbox_selected"
    CHECKBOX_UNSELECTED = "checkbox_unselected"
    CODE = "code"
    FIGURE = "picture"
    FOOTNOTE = "footnote"
    FORMULA = "formula"
    LINE_NUM = "line_number"
    LIST_ITEM = "list_item"
    LIST = "list"
    PAGE_FOOTER = "page_footer"
    PAGE_HEADER = "page_header"
    PARAGRAPH = "text"
    # PICTURE = "picture"
    REFERENCE = "reference"
    SECTION = "section_header"
    SUBSECTION = "subtitle-level-2"
    SUBSUBSECTION = "subtitle-level-3"
    TABLE = "table"
    TABLE_OF_CONTENTS = "table-of-contents"
    TEXT = "paragraph"
    TITLE = "title"
    INLINE = 'inline'

    _type_names = [
        CAPTION,
        CHECKBOX_SELECTED,
        CHECKBOX_UNSELECTED,
        CODE,
        FIGURE,
        FOOTNOTE,
        FORMULA,
        LINE_NUM,
        LIST_ITEM,
        PAGE_FOOTER,
        PAGE_HEADER,
        PARAGRAPH,
        REFERENCE,
        SECTION,
        SUBSECTION,
        SUBSUBSECTION,
        TABLE,
        TABLE_OF_CONTENTS,
        TEXT,
        TITLE,
        LIST,
        INLINE
    ]

    def has_type_name(type_name: str) -> bool:
        return (type_name in LatexItemTypeNames._type_names)
