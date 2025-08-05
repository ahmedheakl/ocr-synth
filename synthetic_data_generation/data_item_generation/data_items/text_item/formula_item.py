from pylatex import NewLine, Math
from pylatex.utils import NoEscape
from sympy.parsing.latex import parse_latex

from .text_item import TextItem
from synthetic_data_generation.data_structures.latex_document.custom_document import CustomDocument
from synthetic_data_generation.templates.template import Template
from util.latex_item_type_names import LatexItemTypeNames
import time
import re
class FormulaItem(TextItem):
    """
    EquationItem represents an equation (or formula) within the document.
    It is assumed that equation items use a label that corresponds to a formula type
    (e.g. LatexItemTypeNames.FORMULA) and that the equation content (TeX code) is stored in the text attribute.
    """
    def __init__(self, index, data: dict):
        super().__init__(index, data)
        # Optionally, you might check that the label is one that you expect for equations:
        if data.get("label") != LatexItemTypeNames.FORMULA:
            raise ValueError("EquationItem must have a formula label")
    
    def add_as_latex_to_doc(self, doc: CustomDocument):
        """
        Adds the equation to the document using display math mode.
        Here we wrap the equation in \[ ... \] so that it is typeset as a displayed formula.
        """
        # Insert a new line before the equation
        doc.append(NewLine())
        # Using raw LaTeX delimiters is one common way to output equations.
        doc.log_write_position(self._index)
        cut = self.split_equation()
        if cut > 0:
            # print(f'cut {cut}')
            self._text = self._text[0:cut]
            self.find_closest_equation_command()
            doc.append(NoEscape(r"\[ " + self._text + r" \]"))
        else:
            doc.append(NoEscape(r"\[ " + self._text + r" \]"))
        doc.log_write_position(self._index)
        doc.append(NewLine())
        # Log the write position if the item is meant to be included in the reading order.
        excluded_ro_items = Template().get_excluded_reading_order_items()
        # if not excluded_ro_items.has_item(self._type):

    def find_closest_equation_command(self):
        #post processing of a latex equation after cut
        #this is necessary to avoid latex errors.
        text_split = self._text.split('\\')
        self._text = ('\\').join(text_split[0:-1])
        openings = self._text.count('{')
        closening = self._text.count('}')
        diff = max(openings - closening, 0)
        while not self.is_valid_latex_math(self._text + '}') and len(self._text) > 0:
            self._text = self._text[:-1]
        self._text += '}'

    
    def split_equation(self):
        '''We want to split an equation if the number of characters is over
        a certain quantity.
        This is done to have the equations always inside the columns
        '''
        layout_settings = Template().get_layout_settings()
        num_cols = layout_settings.get_num_cols()
        #TODO: start by using an heuristic, should improve.
        if num_cols > 1 and len(self._text) > (40 / num_cols):
            return int(40/num_cols)
        return False
    
    def is_valid_latex_math(self, expr):
        try:
            parse_latex(expr)
        except:
            print('invalid math')

    def is_valid(self):
        cut = self.split_equation()
        if cut > 0:
            # print(f'cut {cut}')
            self._text = self._text[0:cut]
            self.find_closest_equation_command()
        
        if len(self._text) > 1:
            return True
        
        return False



