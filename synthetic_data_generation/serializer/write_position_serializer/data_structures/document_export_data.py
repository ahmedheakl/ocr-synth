import json
import os
from PIL import Image

from synthetic_data_generation.config.config import Config
from synthetic_data_generation.config.config_values import ConfigValues
from synthetic_data_generation.data_stores.target_latex_document_store import TargetLatexDocumentStore
from synthetic_data_generation.serializer.write_position_serializer.pos_logging.items_position_stores_manager import ItemsPositionStoresManager
from util import document_hasher
from util import file_path_manager
from .ground_truth_data import GroundTruthData
from .ground_truth_item import GroundTruthItem
from .page_export_data import PageExportData

class DocumentExportData:

    def __init__(self, synth_doc_file_path: str):
        self._synth_doc_file_path = synth_doc_file_path
        self._data = self._init_page_export_data(synth_doc_file_path)

    def print(self):
        print("========== DOCUMENT EXPORT DATA ==========")
        for _, page_export_data in sorted(self._data.items()):
            page_export_data.print()

    def add_segments(
        self,
        gt_data: GroundTruthData,
        pos_stores_manager: ItemsPositionStoresManager
    ):
        next_segment_index = 0
        for gt_item_index in gt_data.get_indexes(is_sorted=True):
            try:
                gt_item = gt_data.get_item(gt_item_index)
                print("gt_item inside: ", gt_item)
                self._add_gt_item_segments(
                    next_segment_index, gt_item, pos_stores_manager)
                next_segment_index = self._get_next_segment_index(gt_item)
            except:
                print("error")

    # def add_segments(
    #     self,
    #     gt_data: GroundTruthData,
    #     pos_stores_manager: ItemsPositionStoresManager
    # ):
    #     next_segment_index = 0
    #     for gt_item_index in gt_data.get_indexes(is_sorted=True):
    #         # try:
    #         gt_item = gt_data.get_item(gt_item_index)
    #         print("gt_item inside: ", gt_item)
    #         self._add_gt_item_segments(
    #             next_segment_index, gt_item, pos_stores_manager)
    #         next_segment_index = self._get_next_segment_index(gt_item)
    #         # except:
    #         #     print("error")

    def _add_gt_item_segments(
        self,
        next_segment_index: int,
        item: GroundTruthItem,
        pos_stores_manager: ItemsPositionStoresManager
    ):
        for segment in item.to_segments(next_segment_index, pos_stores_manager):
            page_export_data = self._data[segment.get_page_num()]
            page_export_data.add_segment(segment)

    def _get_next_segment_index(self, last_added_item: GroundTruthItem) -> int:
        page_num_of_last_segment = last_added_item.get_end_latex_page_num()
        page_export_data = self._data[page_num_of_last_segment]
        print(page_export_data._synth_doc_name)
        last_segment_added = page_export_data.get_last_segment()
        next_segment_index = last_segment_added.get_index() + 1
        return next_segment_index

    # def _get_next_segment_index(self, last_added_item: GroundTruthItem) -> int:
    #     page_num_of_last_segment = last_added_item.get_end_latex_page_num()
    #     page_export_data = self._data[page_num_of_last_segment]
    #     print(page_export_data._synth_doc_name)
    #     last_segment_added = page_export_data.get_last_segment()
        
    #     # FIXED: Handle case where no segments exist yet
    #     if last_segment_added is None:
    #         print(f"No segments found in page {page_num_of_last_segment}, starting with index 0")
    #         return 0
        
    #     next_segment_index = last_segment_added.get_index() + 1
    #     return next_segment_index

    def add_page_images(self):
        doc_hash = document_hasher.gen_doc_hash(self._synth_doc_file_path)
        page_images = self._load_synth_doc_page_images()
        for page_num, page_image in enumerate(page_images, start=1):
            page_export_data = self._data[page_num]
            page_export_data.add_page_image(page_image)
            page_export_data.add_doc_and_page_hashes(doc_hash)

    def dump(self):
        self._dump_data_to_json()
        # self._save_page_images()

    def _dump_data_to_json(self):
        with open(self._gen_json_dump_file_path(), "w") as fp:
            json.dump({"data": self._gen_json_dump_data()}, fp)

    def _gen_json_dump_file_path(self) -> str:
        file_name = (file_path_manager.extract_fname_wo_ext(
            self._synth_doc_file_path) +
            ConfigValues.HF_DATASET_FNAME_TRAILER + ".json")
        return self._gen_hf_data_doc_dir_path() + file_name

    def _gen_json_dump_data(self) -> list[dict]:
        pages = []
        for page_num in sorted(self._data.keys()):
            page_export_data = self._data[page_num]
            pages.append(page_export_data.to_dict())
        return pages

    def _save_page_images(self):
        for page_num in sorted(self._data.keys()):
            page_export_data = self._data[page_num]
            page_image = page_export_data.get_page_image()
            page_image.save(self._gen_page_image_file_path(page_num))

    def _gen_page_image_file_path(self, page_num: int) -> str:
        dir_path = self._gen_hf_data_doc_dir_path()
        doc_name = file_path_manager.extract_fname_wo_ext(
            self._synth_doc_file_path)
        page_identifier = self._gen_page_image_file_identifier(page_num)
        file_name = doc_name + page_identifier + ".png"
        return dir_path + file_name

    def _gen_page_image_file_identifier(self, page_num: int) -> str:
        return ConfigValues.HF_DATASET_FNAME_TRAILER + f"_page_{page_num}"

    def _gen_hf_data_doc_dir_path(self) -> str:
        file_name = file_path_manager.extract_fname_wo_ext(
            self._synth_doc_file_path)
        dir_path = Config().gen_hf_dataset_storage_dir_path() + file_name + "/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def _init_page_export_data(self, synth_doc_file_path: str) -> dict:
        data = {}
        synth_doc_name = file_path_manager.extract_fname_with_ext(
            synth_doc_file_path)
        num_pages = len(self._load_synth_doc_page_images())
        for page_num in range(1, num_pages + 1):
            data[page_num] = PageExportData(synth_doc_name, page_num)
        return data

    def _load_synth_doc_page_images(self) -> list[Image.Image]:
        dpi = Config().get_export_data_config().get_dpi()
        return TargetLatexDocumentStore().load_page_images(dpi)
