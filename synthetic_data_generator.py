import argparse

from synthetic_data_generation.cleanup.file_cleaner import FileCleaner
from synthetic_data_generation.config.config import Config
from synthetic_data_generation.data_structures.latex_document.custom_document import CustomDocument
from synthetic_data_generation.document_generation.data_stores_manager import DataStoresManager
from synthetic_data_generation.document_generation.document_creator import DocumentCreator
from synthetic_data_generation.document_generation.latex_compilation_exception_handler import LatexCompilationExceptionHandler
from synthetic_data_generation.logging.logger import Logger
from synthetic_data_generation.serializer.write_position_serializer.data_structures.document_export_data import DocumentExportData
from synthetic_data_generation.serializer.write_position_serializer.write_pos_logs_to_json_serializer import WritePosLogsToJsonSerializer
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.templates.template_selectors.template_creation_info import TemplateCreationInfo
from util import file_path_manager
import os
import time
from tqdm import tqdm

def count_files(directory):
    return len([f for f in os.listdir(directory) 
                if os.path.isfile(os.path.join(directory, f))])

class SyntheticDataGenerator:

    def __init__(self, cmd_line_args: argparse.Namespace, config: Config):
        self._cmd_line_args = cmd_line_args
        self._config = config
        self.dataset_path = self._config._dataset_dir_path
        print(self.dataset_path)
        self._template = Template()
        self._data_stores_manager = DataStoresManager()
        self._logger = Logger()
        self._organization_data = OrganizationData()
        # self._selected_doc_file_names = (self._config.
        #     get_selected_doc_file_names())
        self._selected_doc_file_names = []
        start_index = self._config.get_doc_start_index()
        print("start index: ", start_index)
        finish_index = self._config.get_doc_finish_index()
        print("finish_index: ", finish_index)

        if self._selected_doc_file_names == []:
            # Get all files in the directory
            all_files = [f for f in os.listdir(self.dataset_path) 
                        if os.path.isfile(os.path.join(self.dataset_path, f))]
            
            # Sort files for consistent ordering
            all_files.sort()
            
            # Update finish_index if it's beyond the number of files
            total_files = len(all_files)
            finish_index = total_files - 1  # -1 because indices are 0-based
            
            # Slice the files from start_index to finish_index (inclusive)
            self._selected_doc_file_names = all_files[start_index:finish_index + 1]
            # print("files are: ", self._selected_doc_file_names)
            print(f"Selected {len(self._selected_doc_file_names)} files from index {start_index} to {finish_index}")
            # print(f"First few files: {self._selected_doc_file_names[:3]}")  # Show first 3 for verification

    def gen_dataset(self):
        self._logger.log_program_start()
        # start_index = self._config.get_doc_start_index()
        # print("start index: ", start_index)
        # finish_index = self._config.get_doc_finish_index()
        # print("finish_index: ", finish_index)
        # exit()
        # for index, doc_file_name in enumerate(
        #     self._selected_doc_file_names[start_index:finish_index+1],
        #     start=start_index
        # ):
        #     self.gen_dataset_for_doc(index, doc_file_name)
        # self._logger.log_latex_file_generation_errors_to_file(
        #     start_index, finish_index)
        for index, doc_file_name in tqdm(enumerate(self._selected_doc_file_names, start=1), 
                                            total=len(self._selected_doc_file_names),
                                            desc="Processing documents"):
            self.gen_dataset_for_doc(index, doc_file_name)
            
        # Note: You'll need to define start_index and finish_index for the logger
        start_index = 1
        finish_index = len(self._selected_doc_file_names)
        self._logger.log_program_end()

    def gen_dataset_for_doc(self, doc_index: int, doc_file_name: str):
        self._logger.log_creating_dataset_for_doc(doc_index, doc_file_name)
        doc_file_path = self._config.gen_doc_file_path(doc_file_name)
        # print(f'path of the docs {doc_file_path}')
        self._data_stores_manager.init_doc_data_stores(doc_file_path)
        template_creation_infos = (self._config.
            get_selected_template_creation_infos())
        for template_creation_info in template_creation_infos:
            # print(doc_file_path)
            # print(self._config)
            print(f'template info {template_creation_info.get_template_data()}')
            self._organization_data.set_gen_files_storage_path(
                self._config.gen_gen_files_storage_path(
                    doc_file_path, template_creation_info.get_template_type()))
            self._organization_data.set_template_name(
                template_creation_info.get_template_name())
            self._gen_dataset_for_template(template_creation_info)
        self._data_stores_manager.clear_data_stores()
        self._logger.log_created_dataset_for_doc()

    def _gen_dataset_for_template(self, info: TemplateCreationInfo):
        self._logger.log_creating_doc_instances_for_template(
            info.get_template_name(), info.get_num_instances())
        for num in range(info.get_num_instances()):
            self._organization_data.set_template_instance_num(num)
            self._gen_data_for_template_instance(info.get_template_data())
        self._logger.log_created_doc_instances_for_template()

    def _gen_data_for_template_instance(self, template_data: dict):
        if (self._cmd_line_args.env == "dev"):
            self._exec_data_set_generation(template_data)
        else:
            self._exec_data_set_generation(template_data)

    def _exec_data_set_generation(self, template_data: dict):
        self._data_stores_manager.init_gen_latex_doc_data_store(
            self._gen_instance_file_storage_path("pdf"))
        self._template.configure(template_data)
        self._try_gen_synth_data_for_template_instance()

    def _try_gen_synth_data_for_template_instance(self):
        num_trials_per_doc = 3
        for num_trial in range(1, num_trials_per_doc + 1):
            try:
                self._gen_synth_data_for_template_instance()
                return
            except Exception as e:
                if (num_trial == num_trials_per_doc): raise e

    def _handle_latex_files_generation_exception(self, exception):
        self._logger.log_error_creating_doc_instance_for_template(
            self._organization_data.get_template_instance_num())
        self._logger.log_latex_file_gen_exception(
            self._organization_data.get_gen_file_name(),
            self._organization_data.get_template_name(),
            exception)
        self._cleanup_all_generated_files()

    def _cleanup_all_generated_files(self):
        FileCleaner().cleanup_files(
            self._gen_instance_file_storage_path(), ignore_config=True)

    def _gen_synth_data_for_template_instance(self):
        """
        Generates the synthetic pdf document alongside its ground truth values.
        The generated data is stored as a .json file (that entails all the GT
        values) and .png images (the document pages).
        """
        doc = DocumentCreator().create_doc()
        # print(f'created document with Document Creator')
        #generate the PDF,aux, log, pow, pwpows, tex and trpos files
        self._gen_files_from_doc(doc)
        doc_file_path = self._gen_instance_file_storage_path("pdf")
        file_done = os.path.isfile(doc_file_path)
        #check if the files were creating correctly before going into the next one
        if file_done:  
            # print(f'exportin gen data from files')
            #obtain all the bounding box informations needed for refinement
            doc_export_data = self._gen_export_data_from_files()
            # print(f'get final synth doc pdf file')
            #add watermark (bounding box would fail if watermark was be added before)
            self._gen_final_synth_doc_pdf_file(doc)
            # print(f'add page images')
            # doc_export_data.add_page_images()
            try:
                # print(f'dump')
                #need to rewrite dump so that it export dockerdocuments json
                doc_export_data.dump()
            except:
                pass
        # print('cleanup')
        self._cleanup_temp_compilation_files()
        self._logger.log_created_doc_instance_for_template(
            self._organization_data.get_template_instance_num())

    def _gen_files_from_doc(self, doc):
        # Must compile twice to use updated logged position values.
        # print(f'starting compilation')
        self._compile_files(doc)
        self._compile_files(doc)
        self._compile_files(doc)
        # print('ending compilation')

    def _gen_export_data_from_files(self) -> DocumentExportData:
        #path for the calculated positions of the elements in the syn file
        pos_log_file_path = self._gen_instance_file_storage_path("pos")
        # print(f'pos log file path {pos_log_file_path}')
        #path where the syn pdf are going to be saved in
        doc_file_path = self._gen_instance_file_storage_path("pdf")
        # print(f'doc pdf storage path {doc_file_path}')
        # print(f'write pos logsJson')
        #return a DocumentExportData, class used to transform (for example)
        #the current latex document into images
        return WritePosLogsToJsonSerializer().log_file_to_export_data(
            pos_log_file_path, doc_file_path)

    def _gen_final_synth_doc_pdf_file(self, doc: CustomDocument):
        is_data_added = doc.add_data_post_position_log_compilation()
        if (is_data_added):
            self._compile_files(doc)

    def _compile_files(self, doc):
        try:
            doc.generate_pdf(
                self._gen_instance_file_storage_path(),
                clean=True,
                clean_tex=True,
                compiler="lualatex")
        except Exception as e:
            print(f'errror {e}')
            print(f'doc type {type(doc)}')
            # LatexCompilationExceptionHandler().handle_compilation_exception(e)

    def _cleanup_temp_compilation_files(self):
        FileCleaner().cleanup_files(self._gen_instance_file_storage_path())

    def _gen_instance_file_storage_path(self, extension: str=None):
        ext = "" if (extension is None) else f".{extension}"
        files_storage_path = self._organization_data.get_gen_files_storage_path()
        template_name = self._organization_data.get_template_name()
        instance_num = self._organization_data.get_template_instance_num()
        return (f"{files_storage_path}_{template_name.replace('-', '_')}_"
            f"{instance_num}{ext}")

class OrganizationData:

    def __init__(self):
        self._files_storage_path = None
        self._template_name = None
        self._template_instance_num = None

    def get_gen_files_storage_path(self) -> str:
        return self._files_storage_path

    def get_gen_file_name(self) -> str:
        return file_path_manager.extract_fname_wo_ext(self._files_storage_path)

    def get_template_name(self) -> str:
        return self._template_name

    def get_template_instance_num(self) -> int:
        return self._template_instance_num

    def set_gen_files_storage_path(self, files_storage_path: str):
        self._files_storage_path = files_storage_path

    def set_template_name(self, template_name: str):
        self._template_name = template_name

    def set_template_instance_num(self, template_instance_num: int):
        self._template_instance_num = template_instance_num

def parse_cmd_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synthetic Data Generator")
    parser.add_argument("-e", "--env", default="dev",
        help="Environment: 'dev' or 'production'")
    parser.add_argument("-c", "--config", required=True,
        help="Path to the configuration JSON file")

    return parser.parse_args()

def main(cmd_line_args: argparse.Namespace):
    config = Config(config_file_path=cmd_line_args.config)
    SyntheticDataGenerator(cmd_line_args, config).gen_dataset()

if __name__ == "__main__":
    main(parse_cmd_line_args())