from pylatex import UnsafeCommand

class FontCommandsCreator:

    def create_color_command(color: str):
        return UnsafeCommand("color", arguments=color)

    def create_size_command(size: str):
        return UnsafeCommand(size)

    def create_style_command(font_family: str, packages: list=None):
        return UnsafeCommand("fontfamily", arguments=font_family,
            packages=packages)

    def create_select_font_command():
        return UnsafeCommand("selectfont")
