class TemplateValues:

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"

    SIZE_RANDOM = 0
    SIZE_DEFAULT = 5
    SIZE_MIN = 1
    SIZE_MAX = 10

    RANDOM_IDENTIFIER_INT = 0
    RANDOM_IDENTIFIER_FLOAT = 0.0
    RANDOM_IDENTIFIER_STR = "random"

    FLOAT_POSITIONS_LOWER = ["c", "l", "r"]
    FLOAT_POSITIONS_UPPER = ["C", "L", "R"]

    def is_random_identifier_int(value: int) -> bool:
        return value == TemplateValues.RANDOM_IDENTIFIER_INT

    def is_random_identifier_float(value: float) -> bool:
        return value == TemplateValues.RANDOM_IDENTIFIER_FLOAT

    def is_random_identifier_str(value: str) -> bool:
        return value == TemplateValues.RANDOM_IDENTIFIER_STR

    def is_size_valid(size: str) -> bool:
        if (type(size) != int):
            return False
        if (TemplateValues.is_random_identifier_int(size)):
            return True
        return ((size >= TemplateValues.SIZE_MIN) and
            (size <= TemplateValues.SIZE_MAX))

    def clip_size_value(value: int) -> int:
        v = min(TemplateValues.SIZE_MAX, value)
        return max(TemplateValues.SIZE_MIN, v)
