import re

class TextCleaner:

    def clean_text(self, text: str) -> str:
        rtext = text.strip()
        rtext = self.replace_chars_conflicting_with_latex(rtext)
        return self.clean_superscripts(rtext)

    def replace_chars_conflicting_with_latex(self, text: str) -> str:
        text = text.replace("%", "-") # Latex breaks lines at "%".
        return text

    def clean_superscripts(self, text: str) -> str:
        pattern = r"\$.\{([^\}]*)\}\$"
        return re.sub(pattern, r"\1", text)
