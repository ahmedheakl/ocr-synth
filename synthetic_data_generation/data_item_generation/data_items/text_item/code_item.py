from pylatex import NewLine, NoEscape
from pylatex.utils import escape_latex

from synthetic_data_generation.data_structures.latex_document.custom_document import CustomDocument
from synthetic_data_generation.templates.template import Template
from .text_item import TextItem
from util.latex_item_type_names import LatexItemTypeNames
import random

class CodeItem(TextItem):
    def __init__(self, index, data: dict):
        super().__init__(index, data)
        if data.get("label") != LatexItemTypeNames.CODE:
            raise ValueError("CodeItem must have a code label")

    def add_as_latex_to_doc(self, doc: CustomDocument):
        doc.append(NewLine())
        doc.log_write_position(self._index)

        lang = self.detect_language().lower()
        code = self._text.strip()

        bg_color = random.choice(["gray!5", "blue!5", "yellow!10", "green!10", "pink!5"])
        border_color = random.choice(["black!60", "blue!80", "red!60", "gray!80", "purple!70"])

        # Choose rendering style based on language
        if lang in {"python", "bash", "c++", "java", "html", "javascript", "json"}:
            style = random.choice(["minted", "lstlisting"])
        else:
            style = "verbatim"

        if style == "minted":
            doc.append(NoEscape(
                r"\begin{dynamiccodeboxminted}{" + bg_color + "}{" + border_color + "}{" + lang + "}"
            ))
            doc.append(NoEscape(code))
            doc.append(NoEscape(r"\end{dynamiccodeboxminted}"))

        elif style == "lstlisting":
            doc.append(NoEscape(
                r"\begin{dynamiccodeboxlisting}{" + bg_color + "}{" + border_color + "}{" + lang + "}"
            ))
            doc.append(NoEscape(code))
            doc.append(NoEscape(r"\end{dynamiccodeboxlisting}"))

        else:
            doc.append(NoEscape(
                r"\begin{verbatimcodebox}{" + bg_color + "}{" + border_color + "}"
            ))
            doc.append(escape_latex(code))
            doc.append(NoEscape(r"\end{verbatimcodebox}"))

        doc.log_write_position(self._index)
        doc.append(NewLine())

    def detect_language(self) -> str:
        # Placeholder for real language detection logic
        return "text"  # Return "text" to trigger verbatim fallback