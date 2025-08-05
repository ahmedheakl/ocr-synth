import os
from pathlib import Path

from synthetic_data_generation.config.config import Config
from synthetic_data_generation.data_item_generation.data_items.figure_item import figure_item_image_saver

class FileCleaner:

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            cls._instance = super(FileCleaner, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if (self._initialized): return
        self._initialized = True
        self._config = Config()

    def rmdir_recursively(self, dir_path: str):
        if not (os.path.isdir(dir_path)): return
        directory = Path(dir_path)
        for item in directory.iterdir():
            if item.is_dir():
                self.rmdir_recursively(item)
            else:
                item.unlink()
        directory.rmdir()

    def cleanup_files(self, file_path: str, ignore_config: bool=False):
        self._cleanup_temporary_figure_images()
        self._cleanup_latex_files(file_path, ignore_config)

    def _cleanup_temporary_figure_images(self):
        dir_path = figure_item_image_saver.get_figure_dir_path()
        self.rmdir_recursively(dir_path)

    def _cleanup_latex_files(self, file_path: str, ignore_config: bool):
        if (self._config.clean_aux_files() or ignore_config):
            self.cleanup_aux_file(file_path)
        if (self._config.clean_log_files() or ignore_config):
            self.cleanup_log_file(file_path)
        if (self._config.clean_tex_files() or ignore_config):
            self.cleanup_tex_file(file_path)
        if (self._config.clean_pdf_files() or ignore_config):
            self.cleanup_pdf_file(file_path)
        if (self._config.clean_pos_files() or ignore_config):
            self.cleanup_pos_file(file_path)
        if (self._config.clean_vis_gt_files() or ignore_config):
            self.cleanup_vis_gt_file(file_path)

    def cleanup_aux_file(self, file_path: str):
        self._cleanup_file(file_path, "aux")

    def cleanup_log_file(self, file_path: str):
        self._cleanup_file(file_path, "log")

    def cleanup_tex_file(self, file_path: str):
        self._cleanup_file(file_path, "tex")

    def cleanup_pdf_file(self, file_path: str):
        self._cleanup_file(file_path, "pdf")

    def cleanup_pos_file(self, file_path: str):
        self.cleanup_main_text_item_pos_file(file_path)
        self.cleanup_pagaraph_word_pos_file(file_path)
        self.cleanup_table_row_pos_file(file_path)

    def cleanup_main_text_item_pos_file(self, file_path: str):
        self._cleanup_file(file_path, "pos")

    def cleanup_pagaraph_word_pos_file(self, file_path: str):
        self._cleanup_file(file_path, "pwpos")

    def cleanup_table_row_pos_file(self, file_path: str):
        self._cleanup_file(file_path, "trpos")

    def cleanup_vis_gt_file(self, file_path: str):
        self._cleanup_file(file_path, "json")

    def _cleanup_file(self, path: str, extension: str):
        file_path = f"{path}.{extension}"
        if (os.path.isfile(file_path)):
            os.unlink(file_path)
