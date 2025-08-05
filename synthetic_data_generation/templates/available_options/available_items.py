from copy import deepcopy

class AvailableItems:

    TITLE = "title"
    SUBTITLE_LEVEL_1 = "subtitle-level-1"
    SUBTITLE_LEVEL_2 = "subtitle-level-2"
    SUBTITLE_LEVEL_3 = "subtitle-level-3"
    PARAGRAPH = "paragraph"
    FIGURE = "figure"
    TABLE = "table"
    CAPTION = "caption"
    PAGE_HEADER = "page-header"
    SECTION = "section_header"
    PAGE_FOOTER = "page-footer"
    LIST_ITEMS = "list-item"


    _items = [
        TITLE,
        SUBTITLE_LEVEL_1,
        SUBTITLE_LEVEL_2,
        SUBTITLE_LEVEL_3,
        PARAGRAPH,
        FIGURE,
        TABLE,
        CAPTION,
        PAGE_HEADER,
        PAGE_FOOTER,
        LIST_ITEMS
    ]

    def get_items():
        return deepcopy(AvailableItems._items)

    def has_item(item: str) -> bool:
        return (item in AvailableItems._items)
