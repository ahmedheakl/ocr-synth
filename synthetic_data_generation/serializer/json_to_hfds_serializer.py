import logging
import glob
import os
from datasets import Dataset, DatasetDict
from json.decoder import JSONDecodeError
from PIL import Image

from data_loading.data_loader import DataLoader
from synthetic_data_generation.config.config_values import ConfigValues
from synthetic_data_generation.config.export_data_keys import ExportDataKeys
from synthetic_data_generation.hf_dataset_generation.dataset_generation_config import DatasetGenerationConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JsonToHfdsSerializer:

    def gen_hf_dataset(self):
        ds_gen_config = DatasetGenerationConfig()
        if (ds_gen_config.has_synthetic_data()):
            gen_kwargs = {"ds_gen_config": ds_gen_config}
            dataset = Dataset.from_generator(
                self._gen_hf_dataset, gen_kwargs=gen_kwargs)
            dataset_split = self._gen_dataset_split(
                dataset, ds_gen_config.get_test_split_size())
            dataset_split.save_to_disk(ds_gen_config.get_storage_dir_path())
        else:
            logger.info("No data available for HF dataset generation!")

    def _gen_dataset_split(
        self, dataset: Dataset, test_size: float
    ) -> DatasetDict:
        if (test_size == 0):
            dataset_dict = DatasetDict()
            dataset_dict["train"] = dataset
            return dataset_dict
        if (test_size == 1):
            dataset_dict = DatasetDict()
            dataset_dict["test"] = dataset
            return dataset_dict
        return dataset.train_test_split(test_size=test_size)

    def _gen_hf_dataset(self, ds_gen_config: DatasetGenerationConfig):
        for ds_config in ds_gen_config.get_dataset_configs():
            continue_with_next_ds_config = False
            num_generated_pages = 0
            ds_path = ds_config.get_dataset_path()
            for dir_name in sorted(ds_config.get_synthetic_data_dir_names()):
                dir_path = os.path.join(ds_path, dir_name)
                doc_data = self._load_json_data(dir_name, dir_path)
                if (doc_data is None): continue
                page_images = self._load_page_images(dir_name, dir_path)
                if (page_images is None): continue
                if not (self._is_data_and_image_len_the_same(
                    doc_data, page_images)): continue
                self._add_page_images_to_data(doc_data, page_images)
                for page_data in doc_data:
                    yield page_data
                    num_generated_pages += 1
                    num_pages = ds_config.get_num_pages_to_load()
                    if (num_pages is None): continue
                    if (num_generated_pages >= num_pages):
                        continue_with_next_ds_config = True
                        break
                if (continue_with_next_ds_config): break

    def _load_json_data(self, doc_name: str, dir_path: str) -> list[dict]:
        file_name = doc_name + ConfigValues.HF_DATASET_FNAME_TRAILER + ".json"
        json_file_path = os.path.join(dir_path, file_name)
        try:
            return DataLoader().load_json_data(json_file_path)["data"]
        except NotADirectoryError:
            logger.exception(f"Data was not created for document.")
        except JSONDecodeError:
            logger.exception(f"Empty json file was created for document.")
        except:
            logger.exception("Other json file loading error.")
        return None

    def _load_page_images(
        self, doc_name: str, dir_path: str
    ) -> list[Image.Image]:
        page_images = []
        file_name_begin = (doc_name + ConfigValues.HF_DATASET_FNAME_TRAILER +
            ConfigValues.HF_DATASET_PAGE_NUM_TRAILER)
        file_path_begin = os.path.join(dir_path, file_name_begin)
        file_path_end = ".png"
        num_page_images = len(glob.glob(f"{file_path_begin}*.png"))
        try:
            for page_num in range(1, num_page_images + 1):
                file_path = file_path_begin + str(page_num) + file_path_end
                page_image = Image.open(file_path)
                page_images.append(page_image)
            return page_images
        except IOError:
            logger.exception("Too many files open (doc has too many pages).")
            return None

    def _is_data_and_image_len_the_same(
        self, data: list[dict], page_images: list[Image.Image]
    ) -> bool:
        if (len(data) == len(page_images)):
            return True
        logger.warning("Data length and number of page images different.")
        return False

    def _get_file_paths(self, dir_path: str) -> list[str]:
        fnames = f"{dir_path}*{ConfigValues.HF_DATASET_FNAME_TRAILER}.json"
        return glob.glob(fnames)

    def _add_page_images_to_data(
        self, data: list[dict], page_images: list[Image.Image]
    ):
        for page_num in range(len(data)):
            data[page_num][ExportDataKeys.IMAGE] = page_images[page_num]
