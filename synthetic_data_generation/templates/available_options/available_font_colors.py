from random import choice
from synthetic_data_generation.templates.util.template_values import TemplateValues

class AvailableFontColors:
    _available_colors = [
        "red", "green", "blue", "cyan", "magenta", "black", "gray", "darkgray",
        "brown", "olive", "orange", "purple", "teal", "violet", "yellow", "white"
    ]
    _default_color = "black"

    @staticmethod
    def get_this_or_default_color(color: str) -> str:
        if TemplateValues.is_random_identifier_str(color):
            return AvailableFontColors.get_random_color()
        if color in AvailableFontColors._available_colors:
            return color
        return AvailableFontColors._default_color

    @staticmethod
    def get_default_color() -> str:
        return AvailableFontColors._default_color

    @staticmethod
    def get_random_color() -> str:
        return choice(AvailableFontColors._available_colors)

    @staticmethod
    def get_all_colors() -> list:
        return AvailableFontColors._available_colors

    @staticmethod
    def is_default_color(color: str) -> bool:
        return AvailableFontColors._default_color == color