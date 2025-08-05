import os

class DatasetConfig:

    def __init__(
        self, dataset_name: str, dataset_path: str, num_pages_to_load: int
    ):
        self._name = dataset_name
        self._path = dataset_path
        self._num_pages_to_load = num_pages_to_load
        self._synthetic_data_dir_names = self._gen_dir_names(dataset_path)

    def get_dataset_name(self) -> str:
        return self._name

    def get_dataset_path(self) -> str:
        return self._path

    def get_num_pages_to_load(self) -> int:
        return self._num_pages_to_load

    def get_synthetic_data_dir_names(self) -> list[str]:
        return self._synthetic_data_dir_names

    def get_num_dir_names(self) -> int:
        return len(self._synthetic_data_dir_names)

    def _gen_dir_names(self, dataset_path: str) -> list[str]:
        dir_names = []
        for item_name in os.listdir(dataset_path):
            path_name = os.path.join(dataset_path, item_name)
            if (os.path.isdir(path_name)):
                dir_names.append(item_name)
        return dir_names
