import random
from pylatex import UnsafeCommand

from synthetic_data_generation.templates.available_options.available_font_colors import AvailableFontColors
from synthetic_data_generation.templates.util.template_keys import TemplateKeys
from synthetic_data_generation.templates.util.template_values import TemplateValues
from synthetic_data_generation.templates.util.template_questioner import TemplateQuestioner

class WatermarkSettings:

    _default_text = "sample"
    _text_choices = [
        _default_text,
        "confidential",
        "copyright",
        "do not copy",
        "draft only",
        "preview",
        "private",
        "sample only",
        "secret",
        "test sample",
        "top secret",
        "watermark"
    ]
    _text_length_min = 5
    _text_length_max = 12
    _color_default = "gray"
    _color_intensity_default = 0.5
    _color_intensity_min = 0.3
    _color_intensity_max = 0.8
    _angle_default = 45 # deg
    _angle_min = 0 # deg
    _angle_max = 360 # deg
    _scale_default = 1.2
    _scale_min = 0.8
    _scale_max = 1.4

    def __init__(self, template: dict):
        watermark_style = TemplateQuestioner(template).get_watermark_style()
        self._is_active = (len(watermark_style) > 0)
        self._text = self._resolve_text(watermark_style)
        self._color = self._resolve_color(watermark_style)
        self._color_intensity = self._resolve_color_intensity(watermark_style)
        self._angle = self._resolve_angle(watermark_style)
        self._scale = self._resolve_scale(watermark_style)

    def are_active(self) -> bool:
        return self._is_active

    def to_latex_commands(self) -> list[UnsafeCommand]:
        return [
            UnsafeCommand("SetWatermarkText", arguments=self._text),
            UnsafeCommand("SetWatermarkAngle", arguments=self._angle),
            UnsafeCommand("SetWatermarkScale", arguments=self._scale),
            self._gen_set_watermark_color_command()
        ]

    def _gen_set_watermark_color_command(self) -> UnsafeCommand:
        if (self._color == WatermarkSettings._color_default):
            return UnsafeCommand("SetWatermarkColor", options=self._color,
                arguments=self._color_intensity)
        return UnsafeCommand("SetWatermarkColor", arguments=self._color)

    def _resolve_text(self, watermark_style: dict) -> str:
        if not (self._is_text_valid(watermark_style)):
            return WatermarkSettings._default_text
        text = watermark_style[TemplateKeys.TEXT]
        if (TemplateValues.is_random_identifier_str(text)):
            return random.choice(WatermarkSettings._text_choices)
        return text[:WatermarkSettings._text_length_max]

    def _is_text_valid(self, watermark_style: dict) -> bool:
        if (TemplateKeys.TEXT not in watermark_style):
            return False
        text = watermark_style[TemplateKeys.TEXT]
        return ((type(text) == str) and
            (len(text) >= WatermarkSettings._text_length_min) and
            (len(text) <= WatermarkSettings._text_length_max))

    def _resolve_color(self, watermark_style: dict) -> str:
        if not (self._is_color_valid(watermark_style)):
            return WatermarkSettings._color_default
        font_color = watermark_style[TemplateKeys.FONT_COLOR]
        color = AvailableFontColors.get_this_or_default_color(font_color)
        if (AvailableFontColors.is_default_color(color)):
            return WatermarkSettings._color_default
        return color

    def _is_color_valid(self, watermark_style: dict) -> bool:
        if (TemplateKeys.FONT_COLOR not in watermark_style):
            return False
        return (type(watermark_style[TemplateKeys.FONT_COLOR]) == str)

    def _resolve_color_intensity(self, watermark_style: dict) -> float:
        if not (self._is_color_intensity_valid(watermark_style)):
            return WatermarkSettings._color_intensity_default
        size = watermark_style[TemplateKeys.COLOR_INTENSITY]
        if (TemplateValues.is_random_identifier_int(size)):
            return random.uniform(WatermarkSettings._color_intensity_min,
                WatermarkSettings._color_intensity_max)
        range = (WatermarkSettings._color_intensity_max -
            WatermarkSettings._color_intensity_min)
        step_size = range / TemplateValues.SIZE_MAX
        num_steps = size
        intensity = (WatermarkSettings._color_intensity_min +
            num_steps * step_size)
        return max(WatermarkSettings._color_intensity_min, intensity)

    def _is_color_intensity_valid(self, watermark_style: dict) -> bool:
        if (TemplateKeys.COLOR_INTENSITY not in watermark_style):
            return False
        size = watermark_style[TemplateKeys.COLOR_INTENSITY]
        return TemplateValues.is_size_valid(size)

    def _resolve_angle(self, watermark_style: dict) -> int:
        if not (self._is_angle_valid(watermark_style)):
            return int(WatermarkSettings._angle_default)
        angle = int(watermark_style[TemplateKeys.ANGLE_DEGREES])
        if (TemplateValues.is_random_identifier_int(angle)):
            return random.randint(0, 360)
        return angle

    def _is_angle_valid(self, watermark_style: dict) -> bool:
        if (TemplateKeys.ANGLE_DEGREES not in watermark_style):
            return False
        angle = watermark_style[TemplateKeys.ANGLE_DEGREES]
        if ((type(angle) != int) and (type(angle) != float)):
            return False
        return ((angle >= WatermarkSettings._angle_min) and
            (angle <= WatermarkSettings._angle_max))

    def _resolve_scale(self, watermark_style: dict) -> float:
        if not (self._is_scale_valid(watermark_style)):
            return self._scale_default
        config_size = watermark_style[TemplateKeys.SIZE]
        if (TemplateValues.is_random_identifier_int(config_size)):
            size = random.randint(
                TemplateValues.SIZE_MIN, TemplateValues.SIZE_MAX)
        else:
            size = config_size
        num_steps = size - 1
        range = (WatermarkSettings._scale_max - WatermarkSettings._scale_min)
        num_steps_max = TemplateValues.SIZE_MAX - 1
        step_size = range / num_steps_max
        scale = WatermarkSettings._scale_min + (num_steps * step_size)
        return min(scale, self._compute_scale_max_for_text_length())

    def _compute_scale_max_for_text_length(self) -> float:
        text_length = len(self._text)
        text_range = (WatermarkSettings._text_length_max -
            WatermarkSettings._text_length_min)
        num_steps = 4
        text_step_size = text_range / num_steps
        text_length_threshold = WatermarkSettings._text_length_min
        steps = num_steps
        while (text_length > text_length_threshold):
            text_length_threshold += text_step_size
            steps -= 1
        num_scale_steps = max(0, steps)
        scale_range = (WatermarkSettings._scale_max -
            WatermarkSettings._scale_min)
        scale_step_size = scale_range / num_steps
        return WatermarkSettings._scale_min + num_scale_steps * scale_step_size

    def _is_scale_valid(self, watermark_style: dict) -> bool:
        if (TemplateKeys.SIZE not in watermark_style):
            return False
        size = watermark_style[TemplateKeys.SIZE]
        return TemplateValues.is_size_valid(size)
