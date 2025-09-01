from pylatex import Document, Package, UnsafeCommand
from pylatex.utils import NoEscape

from synthetic_data_generation.document_extension.command_extension.command_extender import CommandExtender
from synthetic_data_generation.document_extension.package_extension.package_extender import PackageExtender
from synthetic_data_generation.document_extension.type_extension.type_extender import TypeExtender
from synthetic_data_generation.logging.documents.document_write_position_logger import DocumentWritePositionLogger
from synthetic_data_generation.templates.available_options.available_items import AvailableItems
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.templates.template_settings.layout_settings.layout_settings import LayoutSettings
_TIKZ = Package('tikz', options='remember picture,overlay')


class CustomDocument(Document):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._extend()
        from pylatex import Command
        self.packages.append(Package('geometry'))
        # self.preamble.append(NoEscape(r'\newgeometry{margin=0.5cm}'))  # Very tight margins for testing
        self.preamble.append(NoEscape(r'\newgeometry{top=1cm,bottom=2cm,left=1.5cm,right=1.5cm}'))
        self._set_style()
        self._set_line_nums()
        self._write_position_logger = DocumentWritePositionLogger()

    def log_write_position(self, item_index):
        self._write_position_logger.log_position(self, item_index)

    def add_data_post_position_log_compilation(self) -> bool:
        return self._set_watermarks()

    def _extend(self):
        # Add base packages
        PackageExtender().add_base_packages(self)
        # Add base commands and types
        CommandExtender().add_base_commands(self)
        TypeExtender().add_base_types(self)

    def _set_style(self):
        layout_settings = Template().get_layout_settings()
        self._set_background_style(layout_settings)
        self._set_font_color(layout_settings)
        self._set_font_size(layout_settings)
        self._set_font_style(layout_settings)
        self._set_title_style(layout_settings)
        self._set_caption_style(layout_settings)

        self._enforce_rtl_layout()
        
    def _enforce_rtl_layout(self):
        layout_settings = Template().get_layout_settings()
        if layout_settings.is_arabic():
            self.append(NoEscape(r"\RTL"))

        
    def _set_font_color(self, layout_settings: LayoutSettings):
        self.append(UnsafeCommand(
            "color", arguments=layout_settings.get_font_color()))

    def _set_font_size(self, layout_settings: LayoutSettings):
        self.append(UnsafeCommand(
            layout_settings.get_font_size_as_latex_str()))

    def _set_font_style(self, layout_settings: LayoutSettings):
        pass

    def _set_title_style(self, layout_settings: LayoutSettings):
        pass  # Title styling skipped for now

    def _set_caption_style(self, layout_settings: LayoutSettings):
        active_items = Template().get_active_items()
        if active_items.has_item(AvailableItems.FIGURE):
            font_family = layout_settings.get_font_style().get_latex_code()
            self.preamble.append(
                UnsafeCommand(
                    "DeclareCaptionFormat",
                    arguments=[
                        "customcaptionformat",
                        "#1#2#3"  # No font override
                    ]
                )
    )
            
    def _set_background_style(self, ls: LayoutSettings):
        # -------------- SOLID COLOUR -----------------------------------
        if ls.use_background_color():
            self.packages.append(Package('xcolor', options='dvipsnames'))
            self.preamble.append(
                UnsafeCommand('pagecolor', arguments=NoEscape(ls.get_background_color()))
            )
            return                                        # nothing else to do

        # -------------- IMAGE ------------------------------------------
        if ls.use_background_image():
            img = ls.get_background_image_path()
            if not img:
                return                                   # silently ignore
            self.packages.append(Package('background', options='pages=all'))

            # the key difference ↓ : use paper coordinates, no placement shift
            self.preamble.append(
                UnsafeCommand('backgroundsetup',
                    options=NoEscape(
                        r"scale=1,"
                        r"angle=0,"
                        r"opacity=1,"
                        r"position=paper,"
                        r"anchor=paper,"
                        rf"contents={{\includegraphics"
                        r"[width=\paperwidth,height=\paperheight,"
                        r"keepaspectratio=false]{" + img + "}}}"
                    )
                )
            )
        if ls.use_background_gradient():
            # 1. Required packages
            self.packages.append(Package('xcolor', options='dvipsnames'))
            self.packages.append(Package('tikz'))

            # 2. Random gradient colors (assumed already set in layout settings)
            top = ls.get_gradient_top()
            bottom = ls.get_gradient_bottom()

            # 3. Add the TikZ gradient overlay globally
            gradient_code = rf"""
        \AddToShipoutPictureBG*{{
            \begin{{tikzpicture}}[remember picture,overlay]
                \shade[top color={top}, bottom color={bottom}]
                    (current page.south west) rectangle (current page.north east);
            \end{{tikzpicture}}
        }}"""
            self.preamble.append(NoEscape(gradient_code))

    def _set_line_nums(self):
        if Template().get_line_nums_settings().are_displayed():
            PackageExtender().add_line_nums_package(self)
            self.preamble.append(UnsafeCommand("linenumbers"))

    def _set_watermarks(self) -> bool:
        # watermark_settings = Template().get_watermark_settings()
        # if not watermark_settings.are_active():
        #     return False
        # PackageExtender().add_watermark_package(self)
        # for cmd in watermark_settings.to_latex_commands():
        #     self.preamble.append(cmd)
        return False
    