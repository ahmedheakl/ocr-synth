from data_loading.data_loader import DataLoader
from synthetic_data_generation.document.document_selection.document_selector import DocumentSelector
from synthetic_data_generation.templates.template_selectors.template_creation_info import TemplateCreationInfo
from synthetic_data_generation.templates.template_selectors.template_selectors import TemplateSelectors
from util import file_path_manager
from .config_keys import ConfigKeys
from .config_values import ConfigValues
from .document_config_resolver import DocumentConfigResolver
from .export_data_config import ExportDataConfig
from .template_config_resolver import TemplateConfigResolver

import datetime

class Config:
    """
    Reads in the config.json data and provides and interface to this data.
    """

    _instance = None
    _aux_file_ext = "aux"
    _log_file_ext = "log"
    _pdf_file_ext = "pdf"
    _pos_file_ext = "pos"
    _tex_file_ext = "tex"
    _vis_gt_file_ext = "vis"

    def __new__(cls, config_file_path=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
            cls._instance._config_file_path = config_file_path
        return cls._instance

    def __init__(self, config_file_path=None):
        if self._initialized:
            return
        self._initialized = True
        config_data = self._load_config_file(self._config_file_path)
        self._dataset_dir_path = self._resolve_dataset_dir_path(config_data)
        self._doc_start_index = self._resolve_doc_start_index(config_data)
        self._doc_finish_index = self._resolve_doc_finish_index(config_data)
        self._stored_files_status = self._resolve_stored_files_status(
            config_data)
        self._document_selector = self._init_document_selector(config_data)
        self._template_selectors = self._gen_template_selectors(config_data)
        self._export_data_config = ExportDataConfig(config_data)
        self._only_documents_with_tables = config_data['only_documents_with_tables']
        self._cutoff_date = config_data['cutoff_date']

    def get_cutoff_date(self):
        try:
            dt = datetime.fromisoformat(self._cutoff_date)
            return dt
        except ValueError:
            print("Invalid ISO datetime format!")
            return None

    def get_must_have_tables(self):
        return self._only_documents_with_tables

    def get_dataset_dir_path(self) -> str:
        return self._dataset_dir_path

    def gen_doc_file_path(self, doc_file_name: str) -> str:
        return self._dataset_dir_path + doc_file_name

    def gen_gen_files_storage_path(
        self, doc_file_path: str, template_type: str
    ):
        file_name = file_path_manager.extract_fname_wo_ext(doc_file_path)
        gen_dataset_dir_name = template_type
        return (ConfigValues.GENERATED_DATASET_PATH + gen_dataset_dir_name +
            "/" + file_name)

    def gen_hf_dataset_storage_dir_path(self) -> str:
        dir_name = f"index_{self._doc_start_index}_to_{self._doc_finish_index}"
        return ConfigValues.GENERATED_HF_DATASET_PATH + dir_name + "/"

    def get_doc_start_index(self) -> int:
        return self._doc_start_index

    def get_doc_finish_index(self) -> int:
        if (self._doc_finish_index is None):
            return len(self.get_selected_doc_file_names()) - 1
        return self._doc_finish_index

    def has_files_to_create(self) -> bool:
        return self.are_texs_to_be_created()

    def are_texs_to_be_created(self) -> bool:
        return self.keep_tex_files()

    def clean_non_pdf_files(self) -> bool:
        return (self.clean_aux_files() and self.clean_log_files())

    def clean_aux_files(self) -> bool:
        return not self.keep_aux_files()

    def clean_log_files(self) -> bool:
        return not self.keep_log_files()

    def clean_tex_files(self) -> bool:
        return not self.keep_tex_files()

    def clean_pdf_files(self) -> bool:
        return not self.keep_pdf_files()

    def clean_pos_files(self) -> bool:
        return not self.keep_pos_files()

    def clean_vis_gt_files(self) -> bool:
        return not self.keep_vis_gt_files()

    def keep_aux_files(self) -> bool:
        return self._stored_files_status[Config._aux_file_ext]

    def keep_log_files(self) -> bool:
        return self._stored_files_status[Config._log_file_ext]

    def keep_tex_files(self) -> bool:
        return self._stored_files_status[Config._tex_file_ext]

    def keep_pdf_files(self) -> bool:
        return self._stored_files_status[Config._pdf_file_ext]

    def keep_pos_files(self) -> bool:
        return self._stored_files_status[Config._pos_file_ext]

    def keep_vis_gt_files(self) -> bool:
        return self._stored_files_status[Config._vis_gt_file_ext]


    def get_selected_template_creation_infos(
        self
    ) -> list[TemplateCreationInfo]:
        return self._template_selectors.select_template_creation_infos()

    def get_selected_doc_file_names(self) -> list[str]:
        return self._document_selector.select_doc_file_names()

    def get_export_data_config(self) -> ExportDataConfig:
        return self._export_data_config

    def _load_config_file(self, config_file_path: str = None) -> dict:
        if config_file_path is None:
            config_file_path = "synthetic_data_generation/config/config.json"
        return DataLoader().load_json_data(config_file_path)

    def _resolve_dataset_dir_path(self, config_data: dict) -> str:
        key = "dataset-path"
        if (self._is_path_key_valid(key, config_data)):
            return DataLoader().clean_dir_path(config_data[key])
        default_dataset_dir_path = "synthetic_data_generation/dataset/"
        return default_dataset_dir_path

    def _is_path_key_valid(self, key: str, config_data: dict) -> bool:
        return ((key in config_data) and (type(config_data[key]) == str) and
            config_data[key] != "")

    def _resolve_doc_start_index(self, config_data: dict) -> int:
        index = config_data.get(ConfigKeys.DOCUMENT_START_INDEX, 0)
        if ((type(index) == int) and (index >= 0)):
            return index
        raise ValueError("Document start index must be an integral number "
            "greater than or equal to zero.")

    def _resolve_doc_finish_index(self, config_data: dict) -> int:
        index = config_data.get(ConfigKeys.DOCUMENT_FINISH_INDEX, None)
        if ((index is None) or ((type(index) == int) and (index >= 0))):
            return index
        raise ValueError("Document end index must be an integral number "
            "greater than or equal to zero.")

    def _resolve_stored_files_status(self, config_data: dict) -> dict:
        stored_files_status = self._gen_stored_files_status_default()
        stored_files_key = "stored-files"
        if (stored_files_key not in config_data):
            return stored_files_status
        data = config_data[stored_files_key]
        for key in stored_files_status:
            if ((key in data) and (type(data[key]) == bool)):
                stored_files_status[key] = data[key]
        return stored_files_status

    def _gen_stored_files_status_default(self):
        return {
            "aux": False,
            "log": False,
            "pdf": True,
            "pos": False,
            "tex": False,
            "vis": False
        }

    def _init_document_selector(self, config: dict) -> DocumentSelector:
        return DocumentConfigResolver().resolve_doc_selection(config)

    def _gen_template_selectors(self, config: dict) -> TemplateSelectors:
        return TemplateConfigResolver().resolve_templates(config)
