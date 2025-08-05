import os
from pathlib import Path

from util.data_stores.document_page_images_store import DocumentPageImagesStore
from util.data_stores.docling_data_store import DoclingDataStore

_dir_path_base = (f"{os.getcwd()}"
    "/synthetic_data_generation/data_item_generation/"
    "data_items/figure_item/temp_images/")
_extension = "png"

def _get_doc_dir_name() -> str:
    return DocumentPageImagesStore().get_doc_file_name_wo_ext()

def get_figure_dir_path() -> str:
    _file_name_base = DoclingDataStore().get_file_name()
    return _dir_path_base + _get_doc_dir_name() + "/" + _file_name_base + '/'

def gen_figure_path(mti_index) -> str:
    _file_name_base = DoclingDataStore().get_file_name()
    return (get_figure_dir_path() + _file_name_base + f"_{mti_index}." +
        _extension)

def gen_subfigure_path(mti_index, subfigure_index) -> str:
    _file_name_base = DoclingDataStore().get_file_name()
    return (get_figure_dir_path() + _file_name_base +
        f"_{mti_index}_sub_{subfigure_index}." + _extension)

def save_figure_image(image, mti_index):
    Path(get_figure_dir_path()).mkdir(parents=True, exist_ok=True)
    path = gen_figure_path(mti_index)
    image.save(path)

def save_subfigure_image(image, mti_index, subfigure_index):
    Path(get_figure_dir_path()).mkdir(parents=True, exist_ok=True)
    path = gen_subfigure_path(mti_index, subfigure_index)
    image.save(path)
