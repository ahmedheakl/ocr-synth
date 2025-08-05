from pylatex import Figure, Section, Subsection, Subsubsection, Table

from util.latex_item_type_names import LatexItemTypeNames

class PageHeader:
    pass

class Title:
    pass

_data_to_latex_type_map = {
    LatexItemTypeNames.SECTION: Section,
    LatexItemTypeNames.LIST_ITEM: str,
    LatexItemTypeNames.SUBSECTION: Subsection,
    LatexItemTypeNames.SUBSUBSECTION: Subsubsection,
    LatexItemTypeNames.PAGE_HEADER: PageHeader,
    LatexItemTypeNames.PARAGRAPH: str,
    LatexItemTypeNames.TABLE: Table,
    LatexItemTypeNames.TITLE: Title,
    LatexItemTypeNames.FIGURE: Figure
}

def data_to_latex_type(type_: str):
    return _data_to_latex_type_map[type_]

def is_type_section(type_: str):
    latex_type = data_to_latex_type(type_)
    return (latex_type == Section)

def is_type_subsection(type_: str):
    latex_type = data_to_latex_type(type_)
    return (latex_type == Subsection)

def is_type_subsubsection(type_: str):
    latex_type = data_to_latex_type(type_)
    return (latex_type == Subsubsection)

def is_a_section_type(type_: str):
    return (is_type_section(type_) or
            is_type_subsection(type_) or
            is_type_subsubsection(type_))

def is_page_header(type_: str):
    return (_data_to_latex_type_map[type_] == PageHeader)

def is_title(type_: str):
    return (_data_to_latex_type_map[type_] == Title)
