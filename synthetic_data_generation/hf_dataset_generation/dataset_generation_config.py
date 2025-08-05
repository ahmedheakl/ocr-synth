import json

from synthetic_data_generation.hf_dataset_generation.dataset_config import DatasetConfig

class DatasetGenerationConfig:

    _config_file_path = ("./synthetic_data_generation/"
        "hf_dataset_generation/config/config.json")

    def __init__(self):
        config_file_data = self._load_config_file()
        self._dataset_configs = self._gen_dataset_configs(config_file_data)
        self._test_split_size = config_file_data["test-split-size"]
        self._storage_dir_path = config_file_data["storage-dir-path"]

    def get_dataset_configs(self) -> list[DatasetConfig]:
        return self._dataset_configs

    def get_test_split_size(self) -> float:
        return self._test_split_size

    def get_storage_dir_path(self) -> str:
        return self._storage_dir_path

    def get_num_dir_names_of_synthetic_docs(self) -> int:
        num_dir_paths = 0
        for dataset_config in self._dataset_configs:
            num_dir_paths += dataset_config.get_num_dir_names()
        return num_dir_paths

    def has_synthetic_data(self) -> bool:
        return (self.get_num_dir_names_of_synthetic_docs() > 0)

    def _load_config_file(self) -> dict:
        with open(DatasetGenerationConfig._config_file_path, "r") as fp:
            data = json.load(fp)
        return data

    def _gen_dataset_configs(
        self, config_file_data: dict
    ) -> list[DatasetConfig]:
        dataset_configs = []
        for dataset_info in config_file_data["datasets"]:
            dataset_configs.append(
                DatasetConfig(
                    dataset_info["name"],
                    dataset_info["path"],
                    dataset_info["num-pages-to-load"]))
        return dataset_configs
