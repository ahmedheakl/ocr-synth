from PIL import Image

from synthetic_data_generation.data_item_generation.data_items.figure_item import figure_item_image_saver as figure_saver
from synthetic_data_generation.document_extension.environments.table_environments.multicols_all_col_table_env import MulticolsAllColTableEnv
from synthetic_data_generation.templates.template import Template

class FigureItemEnvWidthCalculator:

    def __init__(self):
        self._layout_settings = Template().get_layout_settings()

    def calc_figure_env_line_width(self, env, item_index: int) -> float:
        if (self._is_figure_env_width_invalid(env)):
            image = Image.open(figure_saver.gen_figure_path(item_index))
            if (self._is_big_figure(env, image)):
                return self._calculate_big_figure_env_line_width(image)
            if (self._is_small_figure(env, image)):
                return self._calculate_small_figure_env_line_width(env, image)
        return env.get_line_width()

    def _is_figure_env_width_invalid(self, env) -> bool:
        return ((self._layout_settings.has_one_col()) or
            (type(env) == MulticolsAllColTableEnv))

    def _is_big_figure(self, env, image: Image) -> bool:
        env_line_width = self._calc_env_line_width(env)
        image_height_to_width_ratio = image.height / image.width
        image_env_height = image_height_to_width_ratio * env_line_width
        image_env_height_max = self._calc_image_env_height_max()
        return (image_env_height > image_env_height_max)

    def _is_small_figure(self, env, image: Image) -> bool:
        return image.width < self._calc_env_line_width(env)

    def _calculate_big_figure_env_line_width(self, image: Image) -> float:
        image_env_width_max = ((image.width / image.height) *
            self._calc_image_env_height_max())
        return image_env_width_max / self._layout_settings.get_text_width_px()

    def _calculate_small_figure_env_line_width(
        self, env, image: Image
    ) -> float:
        min_line_width = 0.33 # Images occupy min. a third of the text width.
        env_line_width = self._calc_env_line_width(env)
        if ((image.width / env_line_width) < min_line_width):
            return min_line_width
        return image.width / self._layout_settings.get_text_width_px()

    def _calc_image_env_height_max(self) -> float:
        return 0.5 * self._layout_settings.get_text_height_px()

    def _calc_env_line_width(self, env) -> float:
        return env.get_line_width() * self._layout_settings.get_text_width_px()
