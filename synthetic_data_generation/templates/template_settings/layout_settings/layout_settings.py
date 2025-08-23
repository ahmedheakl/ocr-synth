# from copy import deepcopy
# import random
# import os
# import random
# import glob

# from synthetic_data_generation.templates.available_options.available_font_colors import AvailableFontColors
# from synthetic_data_generation.templates.available_options.available_font_sizes import AvailableFontSizes
# from synthetic_data_generation.templates.available_options.available_font_styles import AvailableFontStyles
# from synthetic_data_generation.templates.latex_page_layout_calculator import LatexPageLayoutCalculator
# from synthetic_data_generation.templates.page_cols_bboxes_generator import PageColsBboxesGenerator
# from synthetic_data_generation.templates.util.font_style import FontStyle
# from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner
# from synthetic_data_generation.templates.util.template_values import TemplateValues
# from synthetic_data_generation.templates.util.template_keys import TemplateKeys
# from synthetic_data_generation.util.unit_converter import UnitConverter
# from .content_cols_configurer import ContentColsConfigurer

# class LayoutSettings:

#     NUM_TABLE_ROWS_MAX_MULTICOL_LAYOUT = 14
#     NUM_TABLE_COLS_MAX_MULTICOL_LAYOUT = 2

#     def __init__(self, template: dict):
#         self._unit_converter = UnitConverter()
#         self._configure(template)
#         self._configure_background(template)


#     def _configure_background(self, template):
#         """
#         Configure background style: solid color or image, with safety and fallback.
#         """
#         self._background_mode = template.get("background-mode", random.choice(["color", "gradient"]))
#         raw_path = template.get("background_image_path", "")
#         self._background_image_path = ""  # Reset default

#         # ---- Color palette ----
#         bg_candidates = [
#             "white", "gray!10", "gray!20", "blue!5", "yellow!10", "pink!10",
#             "red!10", "green!5", "cyan!5", "orange!10", "violet!10", "teal!10", "magenta!10"
#         ]

#         def color_clash(bg, fg):
#             clash_sets = {
#                 ("white", "white"),
#                 ("gray!10", "gray"), ("gray!10", "darkgray"),
#                 ("gray!20", "gray"), ("gray!20", "darkgray"),
#                 ("blue!5", "blue"),
#                 ("yellow!10", "yellow"),
#                 ("black", "black"),
#                 ("pink!10", "red"), ("red!10", "red"),
#                 ("cyan!5", "cyan"), ("green!5", "green"),
#                 ("orange!10", "orange"), ("violet!10", "violet"),
#                 ("teal!10", "teal"), ("magenta!10", "magenta")
#             }
#             return (bg, fg) in clash_sets or (fg, bg) in clash_sets

#         # ---- Mode: solid color ----
#         if self._background_mode == "color":
#             raw_color = template.get("background-color", "random")
#             if raw_color != "random":
#                 self._background_color = raw_color
#             else:
#                 safe_bg_colors = [
#                     color for color in bg_candidates
#                     if color != self._font_color and not color_clash(color, self._font_color)
#                 ]
#                 weights = [5 if c == "white" else 1 for c in safe_bg_colors]
#                 self._background_color = random.choices(safe_bg_colors, weights=weights, k=1)[0]

#         # ---- Mode: image (from file or folder) ----
#         elif self._background_mode == "gradient":
#             gradient_candidates = [
#                 "blue!5", "cyan!5", "pink!10",
#                 "orange!10", "yellow!10", "green!10", "teal!10", "violet!10", "magenta!10"
#             ]

#             # Optional: weight toward lighter tops
#             weights_top = [1 if c.startswith("white") or "gray!5" in c else 1 for c in gradient_candidates]
#             weights_bottom = [1] * len(gradient_candidates)

#             self._grad_top = random.choices(gradient_candidates, weights=weights_top, k=1)[0]
#             self._grad_bottom = random.choices(gradient_candidates, weights=weights_bottom, k=1)[0]
        
#     def _color_clash(self, bg, fg):
#         clash_pairs = [
#             ("white", "white"), ("gray!10", "black"), ("blue!5", "blue"),
#             ("yellow!10", "yellow"), ("gray!20", "gray")
#         ]
#         return (bg, fg) in clash_pairs or (fg, bg) in clash_pairs

#     def use_background_image(self):
#         return self._background_mode == "image"

#     def get_background_image_path(self):
#         return self._background_image_path

#     def use_background_color(self):
#         return self._background_mode == "color"

#     def get_background_color(self):
#         return self._background_color

#     def get_background_color(self):
#         return self._background_color
#     def get_gradient_top(self):
#         return self._grad_top

#     def get_gradient_bottom(self):
#         return self._grad_bottom

#     def use_gradient(self):
#         return self._use_gradient

#     def use_background_gradient(self):     return self._background_mode == "gradient"
#     def get_gradient_top(self):            return self._grad_top
#     def get_gradient_bottom(self):         return self._grad_bottom

#     def is_page_format_landscape(self):
#         return self._page_format == TemplateValues.LANDSCAPE

#     def get_page_size_px(self):
#         return (self.get_page_width_px(), self.get_page_height_px())

#     def get_page_width_pt(self):
#         return self._page_width

#     def get_page_width_px(self):
#         return self._unit_converter.pt_to_px(self._page_width)

#     def get_page_width_sp(self):
#         return self._unit_converter.pt_to_sp(self._page_width)

#     def get_page_height_pt(self):
#         return self._page_height

#     def get_page_height_px(self):
#         return self._unit_converter.pt_to_px(self._page_height)

#     def get_page_height_sp(self):
#         return self._unit_converter.pt_to_sp(self._page_height)

#     def get_head_top_px(self):
#         return self._unit_converter.pt_to_px(self._head_top)

#     def get_foot_top_px(self):
#         return self._unit_converter.pt_to_px(self._foot_top)

#     def get_baseline_skip_px(self):
#         return self._unit_converter.pt_to_px(self._baseline_skip)

#     def has_one_col(self):
#         return self._num_cols == 1

#     def has_multiple_cols(self):
#         return self._num_cols > 1

#     def get_num_cols(self):
#         return self._num_cols

#     def get_col_sep_pt(self):
#         return self._col_sep

#     def get_col_sep_px(self):
#         return self._unit_converter.pt_to_px(self._col_sep)

#     def get_col_width_pt(self):
#         return self._col_width

#     def get_col_width_px(self):
#         return self._unit_converter.pt_to_px(self._col_width)

#     def get_page_cols_bboxes(self, page_num: int):
#         if (self.is_even_page(page_num)):
#             return deepcopy(self._even_page_cols_bboxes)
#         return deepcopy(self._odd_page_cols_bboxes)

#     def get_text_parindent_pt(self):
#         return self._text_parindent

#     def get_text_parindent_px(self):
#         return self._unit_converter.pt_to_px(self._text_parindent)

#     def get_text_parindent_sp(self):
#         return self._unit_converter.pt_to_sp(self._text_parindent)

#     def get_text_width_pt(self):
#         return self._text_width

#     def get_text_width_px(self):
#         return self._unit_converter.pt_to_px(self._text_width)

#     def get_text_height_px(self):
#         return self._unit_converter.pt_to_px(self._text_height)

#     def get_font_size_sp(self):
#         return self._unit_converter.pt_to_sp(self._font_size)

#     def get_font_size_px(self):
#         return self._unit_converter.pt_to_px(self._font_size)

#     def get_section_size_sp(self):
#         return self._unit_converter.pt_to_sp(self._font_size + 6)

#     def get_page_text_x_origin_pt(self, page_num):
#         if (self.is_even_page(page_num)):
#             return self.get_even_page_text_x_origin_pt()
#         return self.get_odd_page_text_x_origin_pt()

#     def get_page_text_x_origin_px(self, page_num):
#         if (self.is_even_page(page_num)):
#             return self.get_even_page_text_x_origin_px()
#         return self.get_odd_page_text_x_origin_px()

#     def get_page_text_x_origin_sp(self, page_num):
#         if (self.is_even_page(page_num)):
#             return self.get_even_page_text_x_origin_sp()
#         return self.get_odd_page_text_x_origin_sp()

#     def get_page_text_x_end_pt(self, page_num):
#         if (self.is_even_page(page_num)):
#             return self.get_even_page_text_x_end_pt()
#         return self.get_odd_page_text_x_end_pt()

#     def get_page_text_x_end_px(self, page_num):
#         if (self.is_even_page(page_num)):
#             return self.get_even_page_text_x_end_px()
#         return self.get_odd_page_text_x_end_px()

#     def get_page_text_x_end_sp(self, page_num):
#         if (self.is_even_page(page_num)):
#             return self.get_even_page_text_x_end_sp()
#         return self.get_odd_page_text_x_end_sp()

#     def get_even_page_text_x_origin_pt(self):
#         return self._even_page_text_x_origin

#     def get_even_page_text_x_origin_px(self):
#         return self._unit_converter.pt_to_px(self._even_page_text_x_origin)

#     def get_even_page_text_x_origin_sp(self):
#         return self._unit_converter.pt_to_sp(self._even_page_text_x_origin)

#     def get_even_page_text_x_end_pt(self):
#         return self._even_page_text_x_origin + self._text_width

#     def get_even_page_text_x_end_px(self):
#         return self._unit_converter.pt_to_px(
#             self.get_even_page_text_x_end_pt())

#     def get_even_page_text_x_end_sp(self):
#         return self._unit_converter.pt_to_sp(
#             self.get_even_page_text_x_end_pt())

#     def get_odd_page_text_x_origin_pt(self):
#         return self._odd_page_text_x_origin

#     def get_odd_page_text_x_origin_px(self):
#         return self._unit_converter.pt_to_px(self._odd_page_text_x_origin)

#     def get_odd_page_text_x_origin_sp(self):
#         return self._unit_converter.pt_to_sp(self._odd_page_text_x_origin)

#     def get_odd_page_text_x_end_pt(self):
#         return self._odd_page_text_x_origin + self._text_width

#     def get_odd_page_text_x_end_px(self):
#         return self._unit_converter.pt_to_px(self.get_odd_page_text_x_end_pt())

#     def get_odd_page_text_x_end_sp(self):
#         return self._unit_converter.pt_to_sp(self.get_odd_page_text_x_end_pt())

#     def get_text_y_origin_pt(self):
#         return self._text_y_origin

#     def get_text_y_origin_px(self):
#         return self._unit_converter.pt_to_px(self._text_y_origin)

#     def get_text_y_origin_sp(self):
#         return self._unit_converter.pt_to_sp(self._text_y_origin)

#     def get_text_y_end_pt(self):
#         return self._text_y_end

#     def get_text_y_end_px(self):
#         return self._unit_converter.pt_to_px(self.get_text_y_end_pt())

#     def get_text_y_end_sp(self):
#         return self._unit_converter.pt_to_sp(self.get_text_y_end_pt())

#     def is_even_page(self, page_num):
#         return page_num % 2 == 0

#     def get_font_color(self) -> str:
#         return self._font_color

#     def get_font_size_as_int(self) -> int:
#         return self._font_size

#     def get_font_size_as_latex_str(self) -> str:
#         return AvailableFontSizes.int_size_to_latex_str(self._font_size)

#     def get_font_style(self) -> FontStyle:
#         return self._font_style

#     def get_packages(self) -> list:
#         return self._packages

#     def is_gen_chart(self) -> bool:
#         return self.gen_chart_flag

#     def get_language(self):
#         return self._language

#     def is_arabic(self):
#         return self._language.lower() == "arabic"

#     def is_english(self):
#         return self._language.lower() == "english"

#     def _configure(self, template: dict):
#         layout_style = TemplateQuestioner(template).get_layout_style()
#         self._language = template.get("language", "english")

#         self._one_inch = 72

#         self._page_format = layout_style[TemplateKeys.PAGE_FORMAT]
#         self._page_width = layout_style[TemplateKeys.PAGE_WIDTH]
#         self._page_height = layout_style[TemplateKeys.PAGE_HEIGHT]

#         self._text_width = layout_style[TemplateKeys.TEXT_WIDTH]
#         self._text_height = layout_style[TemplateKeys.TEXT_HEIGHT]
#         self._text_parindent = layout_style[TemplateKeys.TEXT_PARINDENT]
#         self._baseline_skip = layout_style[TemplateKeys.BASELINE_SKIP]

#         page_layout_calculator = LatexPageLayoutCalculator()
#         self._odd_page_text_x_origin = (page_layout_calculator.
#             calc_odd_page_text_x_origin(layout_style))
#         self._even_page_text_x_origin = (page_layout_calculator.
#             calc_even_page_text_x_origin(layout_style))
#         self._text_y_origin = (page_layout_calculator.
#             calc_text_y_origin(layout_style))
#         self._text_y_end = (page_layout_calculator.
#             calc_text_y_end(layout_style))

#         self._head_top = page_layout_calculator.calc_head_top(layout_style)
#         self._foot_top = page_layout_calculator.calc_foot_top(layout_style)

#         cc_configurer = ContentColsConfigurer(layout_style)
#         self._num_cols = cc_configurer.configure_num_content_cols()
#         self._col_sep = cc_configurer.configure_col_sep()
#         self._col_width = cc_configurer.configure_col_width()

#         self._font_color = AvailableFontColors.get_this_or_default_color(
#             layout_style[TemplateKeys.FONT_COLOR])
#         self._font_size = self._resolve_font_size(layout_style)

#         style_name = layout_style.get(
#             TemplateKeys.FONT_STYLE,
#             AvailableFontStyles.get_default_font_for_language(self._language)
#         )
#         self._font_style = AvailableFontStyles.font_style_to_instance(style_name)

#         self._packages = layout_style[TemplateKeys.PACKAGES]

#         page_cols_bboxes_generator = PageColsBboxesGenerator(
#             layout_style, self._num_cols, self._col_sep)
#         self._even_page_cols_bboxes = (page_cols_bboxes_generator.
#             gen_even_page_cols_bboxes())
#         self._odd_page_cols_bboxes = (page_cols_bboxes_generator.
#             gen_odd_page_cols_bboxes())
#         self.gen_chart_flag = layout_style[TemplateKeys.CHART_FLAG]

#     def _resolve_font_size(self, layout_style: dict) -> int:
#         font_size = AvailableFontSizes.get_this_or_default_size_as_int(
#             layout_style[TemplateKeys.FONT_SIZE])
#         if (font_size < AvailableFontSizes.FOOTNOTESIZE_INT):
#             return AvailableFontSizes.FOOTNOTESIZE_INT
#         if (font_size > AvailableFontSizes.LARGE_INT):
#             return AvailableFontSizes.LARGE_INT
#         return font_size

#     def is_hebrew(self):
#         return self._language.lower() == "hebrew"

#     def is_rtl_language(self):
#         """Check if the language is right-to-left"""
#         return self._language.lower() in ["arabic", "hebrew"]

#     # Update the font style resolution in _configure method:
#     style_name = layout_style.get(
#         TemplateKeys.FONT_STYLE,
#         AvailableFontStyles.get_default_font_for_language(self._language)
#     )

#     # Update the _resolve_font_size method to handle Hebrew fonts:
#     def _resolve_font_size(self, layout_style: dict) -> int:
#         font_size = AvailableFontSizes.get_this_or_default_size_as_int(
#             layout_style[TemplateKeys.FONT_SIZE])
        
#         # Hebrew fonts often work better with slightly larger sizes
#         if self.is_hebrew() and font_size < AvailableFontSizes.SMALL_INT:
#             return AvailableFontSizes.SMALL_INT
            
#         if (font_size < AvailableFontSizes.FOOTNOTESIZE_INT):
#             return AvailableFontSizes.FOOTNOTESIZE_INT
#         if (font_size > AvailableFontSizes.LARGE_INT):
#             return AvailableFontSizes.LARGE_INT
#         return font_size

from copy import deepcopy
import random
import os
import random
import glob

from synthetic_data_generation.templates.available_options.available_font_colors import AvailableFontColors
from synthetic_data_generation.templates.available_options.available_font_sizes import AvailableFontSizes
from synthetic_data_generation.templates.available_options.available_font_styles import AvailableFontStyles
from synthetic_data_generation.templates.latex_page_layout_calculator import LatexPageLayoutCalculator
from synthetic_data_generation.templates.page_cols_bboxes_generator import PageColsBboxesGenerator
from synthetic_data_generation.templates.util.font_style import FontStyle
from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner
from synthetic_data_generation.templates.util.template_values import TemplateValues
from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.util.unit_converter import UnitConverter
from .content_cols_configurer import ContentColsConfigurer

class LayoutSettings:

    NUM_TABLE_ROWS_MAX_MULTICOL_LAYOUT = 14
    NUM_TABLE_COLS_MAX_MULTICOL_LAYOUT = 2

    def __init__(self, template: dict):
        self._unit_converter = UnitConverter()
        self._configure(template)
        self._configure_background(template)

    def _configure_background(self, template):
        """
        Configure background style: solid color or image, with safety and fallback.
        """
        self._background_mode = template.get("background-mode", random.choice(["color", "gradient"]))
        raw_path = template.get("background_image_path", "")
        self._background_image_path = ""  # Reset default

        # ---- Color palette ----
        bg_candidates = [
            "white", "gray!10", "gray!20", "blue!5", "yellow!10", "pink!10",
            "red!10", "green!5", "cyan!5", "orange!10", "violet!10", "teal!10", "magenta!10"
        ]

        def color_clash(bg, fg):
            clash_sets = {
                ("white", "white"),
                ("gray!10", "gray"), ("gray!10", "darkgray"),
                ("gray!20", "gray"), ("gray!20", "darkgray"),
                ("blue!5", "blue"),
                ("yellow!10", "yellow"),
                ("black", "black"),
                ("pink!10", "red"), ("red!10", "red"),
                ("cyan!5", "cyan"), ("green!5", "green"),
                ("orange!10", "orange"), ("violet!10", "violet"),
                ("teal!10", "teal"), ("magenta!10", "magenta")
            }
            return (bg, fg) in clash_sets or (fg, bg) in clash_sets

        # ---- Mode: solid color ----
        if self._background_mode == "color":
            raw_color = template.get("background-color", "random")
            if raw_color != "random":
                self._background_color = raw_color
            else:
                safe_bg_colors = [
                    color for color in bg_candidates
                    if color != self._font_color and not color_clash(color, self._font_color)
                ]
                weights = [5 if c == "white" else 1 for c in safe_bg_colors]
                self._background_color = random.choices(safe_bg_colors, weights=weights, k=1)[0]

        # ---- Mode: gradient ----
        elif self._background_mode == "gradient":
            gradient_candidates = [
                "blue!5", "cyan!5", "pink!10",
                "orange!10", "yellow!10", "green!10", "teal!10", "violet!10", "magenta!10"
            ]

            # Optional: weight toward lighter tops
            weights_top = [1 if c.startswith("white") or "gray!5" in c else 1 for c in gradient_candidates]
            weights_bottom = [1] * len(gradient_candidates)

            self._grad_top = random.choices(gradient_candidates, weights=weights_top, k=1)[0]
            self._grad_bottom = random.choices(gradient_candidates, weights=weights_bottom, k=1)[0]
        
    def _color_clash(self, bg, fg):
        clash_pairs = [
            ("white", "white"), ("gray!10", "black"), ("blue!5", "blue"),
            ("yellow!10", "yellow"), ("gray!20", "gray")
        ]
        return (bg, fg) in clash_pairs or (fg, bg) in clash_pairs

    def use_background_image(self):
        return self._background_mode == "image"

    def get_background_image_path(self):
        return self._background_image_path

    def use_background_color(self):
        return self._background_mode == "color"

    def get_background_color(self):
        return self._background_color

    def get_gradient_top(self):
        return self._grad_top

    def get_gradient_bottom(self):
        return self._grad_bottom

    def use_background_gradient(self):
        return self._background_mode == "gradient"

    def is_page_format_landscape(self):
        return self._page_format == TemplateValues.LANDSCAPE

    def get_page_size_px(self):
        return (self.get_page_width_px(), self.get_page_height_px())

    def get_page_width_pt(self):
        return self._page_width

    def get_page_width_px(self):
        return self._unit_converter.pt_to_px(self._page_width)

    def get_page_width_sp(self):
        return self._unit_converter.pt_to_sp(self._page_width)

    def get_page_height_pt(self):
        return self._page_height

    def get_page_height_px(self):
        return self._unit_converter.pt_to_px(self._page_height)

    def get_page_height_sp(self):
        return self._unit_converter.pt_to_sp(self._page_height)

    def get_head_top_px(self):
        return self._unit_converter.pt_to_px(self._head_top)

    def get_foot_top_px(self):
        return self._unit_converter.pt_to_px(self._foot_top)

    def get_baseline_skip_px(self):
        return self._unit_converter.pt_to_px(self._baseline_skip)

    def has_one_col(self):
        return self._num_cols == 1

    def has_multiple_cols(self):
        return self._num_cols > 1

    def get_num_cols(self):
        return self._num_cols

    def get_col_sep_pt(self):
        return self._col_sep

    def get_col_sep_px(self):
        return self._unit_converter.pt_to_px(self._col_sep)

    def get_col_width_pt(self):
        return self._col_width

    def get_col_width_px(self):
        return self._unit_converter.pt_to_px(self._col_width)

    def get_page_cols_bboxes(self, page_num: int):
        if (self.is_even_page(page_num)):
            return deepcopy(self._even_page_cols_bboxes)
        return deepcopy(self._odd_page_cols_bboxes)

    def get_text_parindent_pt(self):
        return self._text_parindent

    def get_text_parindent_px(self):
        return self._unit_converter.pt_to_px(self._text_parindent)

    def get_text_parindent_sp(self):
        return self._unit_converter.pt_to_sp(self._text_parindent)

    def get_text_width_pt(self):
        return self._text_width

    def get_text_width_px(self):
        return self._unit_converter.pt_to_px(self._text_width)

    def get_text_height_px(self):
        return self._unit_converter.pt_to_px(self._text_height)

    def get_font_size_sp(self):
        return self._unit_converter.pt_to_sp(self._font_size)

    def get_font_size_px(self):
        return self._unit_converter.pt_to_px(self._font_size)

    def get_section_size_sp(self):
        return self._unit_converter.pt_to_sp(self._font_size + 6)

    def get_page_text_x_origin_pt(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_origin_pt()
        return self.get_odd_page_text_x_origin_pt()

    def get_page_text_x_origin_px(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_origin_px()
        return self.get_odd_page_text_x_origin_px()

    def get_page_text_x_origin_sp(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_origin_sp()
        return self.get_odd_page_text_x_origin_sp()

    def get_page_text_x_end_pt(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_end_pt()
        return self.get_odd_page_text_x_end_pt()

    def get_page_text_x_end_px(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_end_px()
        return self.get_odd_page_text_x_end_px()

    def get_page_text_x_end_sp(self, page_num):
        if (self.is_even_page(page_num)):
            return self.get_even_page_text_x_end_sp()
        return self.get_odd_page_text_x_end_sp()

    def get_even_page_text_x_origin_pt(self):
        return self._even_page_text_x_origin

    def get_even_page_text_x_origin_px(self):
        return self._unit_converter.pt_to_px(self._even_page_text_x_origin)

    def get_even_page_text_x_origin_sp(self):
        return self._unit_converter.pt_to_sp(self._even_page_text_x_origin)

    def get_even_page_text_x_end_pt(self):
        return self._even_page_text_x_origin + self._text_width

    def get_even_page_text_x_end_px(self):
        return self._unit_converter.pt_to_px(
            self.get_even_page_text_x_end_pt())

    def get_even_page_text_x_end_sp(self):
        return self._unit_converter.pt_to_sp(
            self.get_even_page_text_x_end_pt())

    def get_odd_page_text_x_origin_pt(self):
        return self._odd_page_text_x_origin

    def get_odd_page_text_x_origin_px(self):
        return self._unit_converter.pt_to_px(self._odd_page_text_x_origin)

    def get_odd_page_text_x_origin_sp(self):
        return self._unit_converter.pt_to_sp(self._odd_page_text_x_origin)

    def get_odd_page_text_x_end_pt(self):
        return self._odd_page_text_x_origin + self._text_width

    def get_odd_page_text_x_end_px(self):
        return self._unit_converter.pt_to_px(self.get_odd_page_text_x_end_pt())

    def get_odd_page_text_x_end_sp(self):
        return self._unit_converter.pt_to_sp(self.get_odd_page_text_x_end_pt())

    def get_text_y_origin_pt(self):
        return self._text_y_origin

    def get_text_y_origin_px(self):
        return self._unit_converter.pt_to_px(self._text_y_origin)

    def get_text_y_origin_sp(self):
        return self._unit_converter.pt_to_sp(self._text_y_origin)

    def get_text_y_end_pt(self):
        return self._text_y_end

    def get_text_y_end_px(self):
        return self._unit_converter.pt_to_px(self.get_text_y_end_pt())

    def get_text_y_end_sp(self):
        return self._unit_converter.pt_to_sp(self.get_text_y_end_pt())

    def is_even_page(self, page_num):
        return page_num % 2 == 0

    def get_font_color(self) -> str:
        return self._font_color

    def get_font_size_as_int(self) -> int:
        return self._font_size

    def get_font_size_as_latex_str(self) -> str:
        return AvailableFontSizes.int_size_to_latex_str(self._font_size)

    def get_font_style(self) -> FontStyle:
        return self._font_style

    def get_packages(self) -> list:
        return self._packages

    def is_gen_chart(self) -> bool:
        return self.gen_chart_flag

    def get_language(self):
        return self._language

    def is_arabic(self):
        return self._language.lower() == "arabic"

    def is_english(self):
        return self._language.lower() == "english"

    def is_urdu(self):
        return self._language.lower() == "urdu"

    def is_hebrew(self):
        return self._language.lower() == "hebrew"

    def is_rtl_language(self):
        """Check if the language is right-to-left"""
        return self._language.lower() in ["arabic", "hebrew", "urdu"]

    def _configure(self, template: dict):
        layout_style = TemplateQuestioner(template).get_layout_style()
        self._language = template.get("language", "english")

        self._one_inch = 72

        self._page_format = layout_style[TemplateKeys.PAGE_FORMAT]
        self._page_width = layout_style[TemplateKeys.PAGE_WIDTH]
        self._page_height = layout_style[TemplateKeys.PAGE_HEIGHT]

        self._text_width = layout_style[TemplateKeys.TEXT_WIDTH]
        self._text_height = layout_style[TemplateKeys.TEXT_HEIGHT]
        self._text_parindent = layout_style[TemplateKeys.TEXT_PARINDENT]
        self._baseline_skip = layout_style[TemplateKeys.BASELINE_SKIP]

        page_layout_calculator = LatexPageLayoutCalculator()
        self._odd_page_text_x_origin = (page_layout_calculator.
            calc_odd_page_text_x_origin(layout_style))
        self._even_page_text_x_origin = (page_layout_calculator.
            calc_even_page_text_x_origin(layout_style))
        self._text_y_origin = (page_layout_calculator.
            calc_text_y_origin(layout_style))
        self._text_y_end = (page_layout_calculator.
            calc_text_y_end(layout_style))

        self._head_top = page_layout_calculator.calc_head_top(layout_style)
        self._foot_top = page_layout_calculator.calc_foot_top(layout_style)

        cc_configurer = ContentColsConfigurer(layout_style)
        self._num_cols = cc_configurer.configure_num_content_cols()
        self._col_sep = cc_configurer.configure_col_sep()
        self._col_width = cc_configurer.configure_col_width()

        self._font_color = AvailableFontColors.get_this_or_default_color(
            layout_style[TemplateKeys.FONT_COLOR])
        self._font_size = self._resolve_font_size(layout_style)

        # Updated font style resolution to handle Hebrew fonts
        style_name = layout_style.get(
            TemplateKeys.FONT_STYLE,
            AvailableFontStyles.get_default_font_for_language(self._language)
        )
        self._font_style = AvailableFontStyles.font_style_to_instance(style_name)

        self._packages = layout_style[TemplateKeys.PACKAGES]

        page_cols_bboxes_generator = PageColsBboxesGenerator(
            layout_style, self._num_cols, self._col_sep)
        self._even_page_cols_bboxes = (page_cols_bboxes_generator.
            gen_even_page_cols_bboxes())
        self._odd_page_cols_bboxes = (page_cols_bboxes_generator.
            gen_odd_page_cols_bboxes())
        self.gen_chart_flag = layout_style[TemplateKeys.CHART_FLAG]

    def _resolve_font_size(self, layout_style: dict) -> int:
        font_size = AvailableFontSizes.get_this_or_default_size_as_int(
            layout_style[TemplateKeys.FONT_SIZE])
        
        # Hebrew fonts often work better with slightly larger sizes
        if self.is_hebrew() and font_size < AvailableFontSizes.SMALL_INT:
            return AvailableFontSizes.SMALL_INT
        
        # Urdu/Nastaliq fonts need larger sizes for readability
        if self.is_urdu() and font_size < AvailableFontSizes.NORMALSIZE_INT:
            return AvailableFontSizes.NORMALSIZE_INT
            
        if (font_size < AvailableFontSizes.FOOTNOTESIZE_INT):
            return AvailableFontSizes.FOOTNOTESIZE_INT
        if (font_size > AvailableFontSizes.LARGE_INT):
            return AvailableFontSizes.LARGE_INT
        return font_size

    # Add method for Urdu-specific layout adjustments:
    def get_urdu_line_spacing_multiplier(self) -> float:
        """Urdu text needs more line spacing due to vertical extent of characters"""
        if self.is_urdu():
            return 1.4  # 40% more line spacing for Urdu
        return 1.0

    def get_urdu_text_width_adjustment(self) -> float:
        """Urdu may need slightly reduced text width for better readability"""
        if self.is_urdu():
            return 0.95  # 5% reduction in text width
        return 1.0