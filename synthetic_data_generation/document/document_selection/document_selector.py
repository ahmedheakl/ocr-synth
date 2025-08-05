import glob

from util import file_path_manager

class DocumentSelector:

    def __init__(self, dataset_path: str):
        self._dataset_path = dataset_path

    def _resolve_dataset_path(self, dataset_path: str) -> str:
        if (dataset_path[-1] == "/"):
            return dataset_path
        return dataset_path + "/"

    def _get_all_doc_file_names(self) -> list[str]:
        file_names = []
        for file_path in sorted(glob.glob(f"{self._dataset_path}*.json")):
            file_names.append(file_path_manager.
                extract_fname_with_ext(file_path))
        return file_names
