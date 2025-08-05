from random import randint

from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.util.template_values import TemplateValues

class AvailableFontSizes:

    RANDOM_INT = 0
    TINY_INT = 1
    SCRIPTSIZE_INT = 2
    FOOTNOTESIZE_INT = 3
    SMALL_INT = 4
    NORMALSIZE_INT = 5
    LARGE_INT = 6
    XLARGE_INT = 7
    XXLARGE_INT = 8
    HUGE_INT = 9
    XHUGE_INT = 10

    RANDOM = TemplateKeys.RANDOM
    TINY = "tiny"
    SCRIPTSIZE = "scriptsize"
    FOOTNOTESIZE = "footnotesize"
    SMALL = "small"
    NORMALSIZE = "normalsize"
    LARGE = "large"
    XLARGE = "Large"
    XXLARGE = "LARGE"
    HUGE = "huge"
    XHUGE = "Huge"

    DEFAULT_SIZE = NORMALSIZE_INT
    SIZE_MIN = TINY_INT
    SIZE_MAX = XHUGE_INT

    _table = {
        RANDOM_INT: RANDOM,
        TINY_INT: TINY,
        SCRIPTSIZE_INT: SCRIPTSIZE,
        FOOTNOTESIZE_INT: FOOTNOTESIZE,
        SMALL_INT: SMALL,
        NORMALSIZE_INT: NORMALSIZE,
        LARGE_INT: LARGE,
        XLARGE_INT: XLARGE,
        XXLARGE_INT: XXLARGE,
        HUGE_INT: HUGE,
        XHUGE_INT: XHUGE
    }

    def int_size_to_latex_str(size: int) -> str:
        try:
            return AvailableFontSizes._table[size]
        except KeyError:
            return AvailableFontSizes.get_default_size_as_latex_str()

    def get_this_or_default_size_as_int(size: int) -> int:
        if (TemplateValues.is_random_identifier_int(size)):
            return AvailableFontSizes.get_random_size_latex_int()
        if (size in AvailableFontSizes._table):
            return size
        return AvailableFontSizes.DEFAULT_SIZE

    def get_default_size_as_int() -> int:
        return AvailableFontSizes.DEFAULT_SIZE

    def get_default_size_as_latex_str() -> str:
        return AvailableFontSizes._table[AvailableFontSizes.DEFAULT_SIZE]

    def get_random_size_latex_int(min: int=None, max: int=None) -> int:
        min = AvailableFontSizes.SIZE_MIN if min is None else min
        max = AvailableFontSizes.SIZE_MAX if max is None else max
        if min > max:
            min, max = max, min
        return randint(min, max)

    def get_random_size_latex_str(min: int=None, max: int=None) -> str:
        random_size = AvailableFontSizes.get_random_size_latex_int(min, max)
        return AvailableFontSizes._table[random_size]
