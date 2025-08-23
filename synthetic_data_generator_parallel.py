# import argparse
# import sys

# sys.path.append('synthetic_data_generation/chart_rendering/src')

# from synthetic_data_generation.cleanup.file_cleaner import FileCleaner
# from synthetic_data_generation.config.config import Config
# from synthetic_data_generation.data_structures.latex_document.custom_document import CustomDocument
# from synthetic_data_generation.document_generation.data_stores_manager import DataStoresManager
# from synthetic_data_generation.document_generation.document_creator import DocumentCreator
# from synthetic_data_generation.document_generation.latex_compilation_exception_handler import LatexCompilationExceptionHandler
# from synthetic_data_generation.logging.logger import Logger
# from synthetic_data_generation.serializer.write_position_serializer.data_structures.document_export_data import DocumentExportData
# from synthetic_data_generation.serializer.write_position_serializer.write_pos_logs_to_json_serializer import WritePosLogsToJsonSerializer
# from synthetic_data_generation.templates.template import Template
# from synthetic_data_generation.templates.template_selectors.template_creation_info import TemplateCreationInfo
# from util import file_path_manager
# from datetime import datetime

# import os
# from multiprocessing import Pool
# import time

# class SyntheticDataGenerator:

#     def __init__(self, cmd_line_args: argparse.Namespace, config: Config):
#         self._cmd_line_args = cmd_line_args
#         self._config = config
#         self._template = Template()
#         self._data_stores_manager = DataStoresManager()
#         self._logger = Logger()
#         self._organization_data = OrganizationData()
#         self._selected_doc_file_names = (self._config.
#             get_selected_doc_file_names())

#     def gen_dataset_for_doc(self, doc_tuple: tuple):
#         doc_index = doc_tuple[0]
#         doc_file_name =  doc_tuple[1]
#         self._logger.log_creating_dataset_for_doc(doc_index, doc_file_name)
#         doc_file_path = self._config.gen_doc_file_path(doc_file_name)
#         self._data_stores_manager.init_doc_data_stores(doc_file_path)
#         template_creation_infos = (self._config.
#             get_selected_template_creation_infos())
#         for template_creation_info in template_creation_infos:
#             try:
#                 self._organization_data.set_gen_files_storage_path(
#                     self._config.gen_gen_files_storage_path(
#                         doc_file_path, template_creation_info.get_template_type()))
#                 self._organization_data.set_template_name(
#                     template_creation_info.get_template_name())
#                 self._gen_dataset_for_template(template_creation_info)
#             except Exception as e:
#                 print(f'skipping document for {e}')
#         self._data_stores_manager.clear_data_stores()
#         self._logger.log_created_dataset_for_doc()

#     def _gen_dataset_for_template(self, info: TemplateCreationInfo):
#         self._logger.log_creating_doc_instances_for_template(
#             info.get_template_name(), info.get_num_instances())
#         for num in range(info.get_num_instances()):
#             self._organization_data.set_template_instance_num(num)
#             self._gen_data_for_template_instance(info.get_template_data())
#         self._logger.log_created_doc_instances_for_template()

#     def _gen_data_for_template_instance(self, template_data: dict):
#         if (self._cmd_line_args.env == "dev"):
#             self._exec_data_set_generation(template_data)
#         else:
#             self._exec_data_set_generation(template_data)

#     def _exec_data_set_generation(self, template_data: dict):
#         self._data_stores_manager.init_gen_latex_doc_data_store(
#             self._gen_instance_file_storage_path("pdf"))
#         self._template.configure(template_data)
#         self._try_gen_synth_data_for_template_instance()

#     def _try_gen_synth_data_for_template_instance(self):
#         num_trials_per_doc = 3
#         for num_trial in range(1, num_trials_per_doc + 1):
#             try:
#                 self._gen_synth_data_for_template_instance()
#                 return
#             except Exception as e:
#                 if (num_trial == num_trials_per_doc): raise e

#     def _handle_latex_files_generation_exception(self, exception):
#         self._logger.log_error_creating_doc_instance_for_template(
#             self._organization_data.get_template_instance_num())
#         self._logger.log_latex_file_gen_exception(
#             self._organization_data.get_gen_file_name(),
#             self._organization_data.get_template_name(),
#             exception)
#         self._cleanup_all_generated_files()

#     def _cleanup_all_generated_files(self):
#         FileCleaner().cleanup_files(
#             self._gen_instance_file_storage_path(), ignore_config=True)

#     def _gen_synth_data_for_template_instance(self):
#         """
#         Generates the synthetic pdf document alongside its ground truth values.
#         The generated data is stored as a .json file (that entails all the GT
#         values) and .png images (the document pages).
#         """
#         print('creating document')
#         doc = DocumentCreator().create_doc()
#         print(f'created document with Document Creator')

#         #generate the PDF,aux, log, pow, pwpows, tex and trpos files
#         self._gen_files_from_doc(doc)
#         doc_file_path = self._gen_instance_file_storage_path("pdf")
#         file_done = os.path.isfile(doc_file_path)

#         #check if the files were creating correctly before going into the next one
#         if file_done:  
#             print(f'exportin gen data from files')
#             #obtain all the bounding box informations needed for refinement
#             doc_export_data = self._gen_export_data_from_files()
#             print(f'get final synth doc pdf file')
#             #add watermark (bounding box would fail if watermark was be added before)
#             self._gen_final_synth_doc_pdf_file(doc)
#             # print(f'add page images')
#             # doc_export_data.add_page_images()
#             try:
#                 doc_export_data.dump()
#             except:
#                 print('Dumped Except')

#         self._cleanup_temp_compilation_files()
#         self._logger.log_created_doc_instance_for_template(
#             self._organization_data.get_template_instance_num())

#     def _gen_files_from_doc(self, doc):
#         # Must compile twice to use updated logged position values.
#         self._compile_files(doc)
#         self._compile_files(doc)

#     def _gen_export_data_from_files(self) -> DocumentExportData:
#         #path for the calculated positions of the elements in the syn file
#         pos_log_file_path = self._gen_instance_file_storage_path("pos")
#         #path where the syn pdf are going to be saved in
#         doc_file_path = self._gen_instance_file_storage_path("pdf")
#         #return a DocumentExportData, class used to transform (for example)
#         #the current latex document into images
#         return WritePosLogsToJsonSerializer().log_file_to_export_data(
#             pos_log_file_path, doc_file_path)

#     def _gen_final_synth_doc_pdf_file(self, doc: CustomDocument):
#         is_data_added = doc.add_data_post_position_log_compilation()
#         if (is_data_added):
#             self._compile_files(doc)

#     def _compile_files(self, doc):
#         # try:
#         print("compiling doc")
#         # print("--:",doc)
#         print("#########################")
#         try:
#             doc.generate_pdf(
#                 self._gen_instance_file_storage_path(),
#                 clean=self._config.clean_non_pdf_files(),
#                 clean_tex=self._config.clean_tex_files(),
#                 compiler="lualatex")
#             print('done compiling the pdf files')
#         except Exception as e:
#             print(f'errror {e}')

#     def _cleanup_temp_compilation_files(self):
#         FileCleaner().cleanup_files(self._gen_instance_file_storage_path())

#     def _gen_instance_file_storage_path(self, extension: str=None):
#         ext = "" if (extension is None) else f".{extension}"
#         files_storage_path = self._organization_data.get_gen_files_storage_path()
#         template_name = self._organization_data.get_template_name()
#         instance_num = self._organization_data.get_template_instance_num()
#         return (f"{files_storage_path}_{template_name.replace('-', '_')}_"
#             f"{instance_num}{ext}")

# class OrganizationData:

#     def __init__(self):
#         self._files_storage_path = None
#         self._template_name = None
#         self._template_instance_num = None

#     def get_gen_files_storage_path(self) -> str:
#         return self._files_storage_path

#     def get_gen_file_name(self) -> str:
#         return file_path_manager.extract_fname_wo_ext(self._files_storage_path)

#     def get_template_name(self) -> str:
#         return self._template_name

#     def get_template_instance_num(self) -> int:
#         return self._template_instance_num

#     def set_gen_files_storage_path(self, files_storage_path: str):
#         self._files_storage_path = files_storage_path

#     def set_template_name(self, template_name: str):
#         self._template_name = template_name

#     def set_template_instance_num(self, template_instance_num: int):
#         self._template_instance_num = template_instance_num

# def parse_cmd_line_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(description="Synthetic Data Generator")
#     parser.add_argument("-e", "--env", default="dev",
#         help="Environment: 'dev' or 'production'")
#     parser.add_argument("-c", "--config", required=True,
#         help="Path to the configuration JSON file")
#     parser.add_argument("-w", "--workers", type=int, default=os.cpu_count(),
#         help="Number of parallel workers (default: number of CPU cores)")

#     return parser.parse_args()

# def filter_documents_without_tables(documents: list):
#     import json
#     documents_with_tables = []
#     base_path = 'synthetic_data_generation/dataset/demo/chinese'
#     for document in documents:
#         json_path = os.path.join(base_path, document)
#         try:
#             with open(json_path, 'r') as file:
#                 data = json.load(file)
#             if len(data['tables']) > 3:
#                 documents_with_tables.append(document)
#         except:
#             pass
#     print(f'seed documents with tables {len(documents_with_tables)}')
#     return documents_with_tables

# def main(cmd_line_args: argparse.Namespace):
#     config = Config(config_file_path=cmd_line_args.config)
#     selected_doc_file_names = config.get_selected_doc_file_names()
#     index_doc_file_name = enumerate(selected_doc_file_names)
#     num_cores = cmd_line_args.workers
#     generator = SyntheticDataGenerator(cmd_line_args, config)
#     with Pool(processes=num_cores) as pool:
#         pool.map(generator.gen_dataset_for_doc, index_doc_file_name)

# if "__main__" == __name__:
#     main(parse_cmd_line_args())

# import argparse
# import sys

# sys.path.append('synthetic_data_generation/chart_rendering/src')

# from synthetic_data_generation.cleanup.file_cleaner import FileCleaner
# from synthetic_data_generation.config.config import Config
# from synthetic_data_generation.data_structures.latex_document.custom_document import CustomDocument
# from synthetic_data_generation.document_generation.data_stores_manager import DataStoresManager
# from synthetic_data_generation.document_generation.document_creator import DocumentCreator
# from synthetic_data_generation.document_generation.latex_compilation_exception_handler import LatexCompilationExceptionHandler
# from synthetic_data_generation.logging.logger import Logger
# from synthetic_data_generation.serializer.write_position_serializer.data_structures.document_export_data import DocumentExportData
# from synthetic_data_generation.serializer.write_position_serializer.write_pos_logs_to_json_serializer import WritePosLogsToJsonSerializer
# from synthetic_data_generation.templates.template import Template
# from synthetic_data_generation.templates.template_selectors.template_creation_info import TemplateCreationInfo
# from util import file_path_manager
# from datetime import datetime

# import os
# from multiprocessing import Pool
# import time
# from tqdm import tqdm

# def count_files(directory):
#     return len([f for f in os.listdir(directory) 
#                 if os.path.isfile(os.path.join(directory, f))])

# class SyntheticDataGenerator:

#     def __init__(self, cmd_line_args: argparse.Namespace, config: Config):
#         self._cmd_line_args = cmd_line_args
#         self._config = config
#         self.dataset_path = self._config._dataset_dir_path
#         print(self.dataset_path)
#         self._template = Template()
#         self._data_stores_manager = DataStoresManager()
#         self._logger = Logger()
#         self._organization_data = OrganizationData()
#         # Get selected doc file names from config or generate from directory
#         self._selected_doc_file_names = (self._config.
#             get_selected_doc_file_names())
        
#         start_index = self._config.get_doc_start_index()
#         print("start index: ", start_index)
#         finish_index = self._config.get_doc_finish_index()
#         print("finish_index: ", finish_index)

#         if self._selected_doc_file_names == []:
#             # Get all files in the directory
#             all_files = [f for f in os.listdir(self.dataset_path) 
#                         if os.path.isfile(os.path.join(self.dataset_path, f))]
            
#             # Sort files for consistent ordering
#             all_files.sort()
            
#             # Update finish_index if it's beyond the number of files
#             total_files = len(all_files)
#             finish_index = total_files - 1  # -1 because indices are 0-based
            
#             # Slice the files from start_index to finish_index (inclusive)
#             self._selected_doc_file_names = all_files[start_index:finish_index + 1]
#             print(f"Selected {len(self._selected_doc_file_names)} files from index {start_index} to {finish_index}")

#     def gen_dataset(self):
#         """
#         Generate dataset using parallel processing for multiple documents
#         """
#         self._logger.log_program_start()
        
#         # Create tuples of (index, doc_file_name) for parallel processing
#         index_doc_file_name_tuples = list(enumerate(self._selected_doc_file_names, start=1))
        
#         num_cores = self._cmd_line_args.workers
#         print(f"Processing {len(index_doc_file_name_tuples)} documents using {num_cores} workers")
        
#         # Use multiprocessing to process documents in parallel
#         with Pool(processes=num_cores) as pool:
#             # Use tqdm for progress tracking (note: progress updates may not be perfectly accurate due to parallel processing)
#             list(tqdm(
#                 pool.imap(self._gen_dataset_for_doc_wrapper, index_doc_file_name_tuples),
#                 total=len(index_doc_file_name_tuples),
#                 desc="Processing documents"
#             ))
        
#         # Log completion
#         start_index = 1
#         finish_index = len(self._selected_doc_file_names)
#         self._logger.log_program_end()

#     def _gen_dataset_for_doc_wrapper(self, doc_tuple: tuple):
#         """
#         Wrapper method for parallel processing
#         """
#         return self.gen_dataset_for_doc(doc_tuple)

#     def gen_dataset_for_doc(self, doc_tuple: tuple):
#         doc_index = doc_tuple[0]
#         doc_file_name = doc_tuple[1]
#         self._logger.log_creating_dataset_for_doc(doc_index, doc_file_name)
#         doc_file_path = self._config.gen_doc_file_path(doc_file_name)
#         self._data_stores_manager.init_doc_data_stores(doc_file_path)
#         template_creation_infos = (self._config.
#             get_selected_template_creation_infos())
#         for template_creation_info in template_creation_infos:
#             try:
#                 print(f'template info {template_creation_info.get_template_data()}')
#                 self._organization_data.set_gen_files_storage_path(
#                     self._config.gen_gen_files_storage_path(
#                         doc_file_path, template_creation_info.get_template_type()))
#                 self._organization_data.set_template_name(
#                     template_creation_info.get_template_name())
#                 self._gen_dataset_for_template(template_creation_info)
#             except Exception as e:
#                 print(f'skipping document for {e}')
#         self._data_stores_manager.clear_data_stores()
#         self._logger.log_created_dataset_for_doc()

#     def _gen_dataset_for_template(self, info: TemplateCreationInfo):
#         self._logger.log_creating_doc_instances_for_template(
#             info.get_template_name(), info.get_num_instances())
#         for num in range(info.get_num_instances()):
#             self._organization_data.set_template_instance_num(num)
#             self._gen_data_for_template_instance(info.get_template_data())
#         self._logger.log_created_doc_instances_for_template()

#     def _gen_data_for_template_instance(self, template_data: dict):
#         if (self._cmd_line_args.env == "dev"):
#             self._exec_data_set_generation(template_data)
#         else:
#             self._exec_data_set_generation(template_data)

#     def _exec_data_set_generation(self, template_data: dict):
#         self._data_stores_manager.init_gen_latex_doc_data_store(
#             self._gen_instance_file_storage_path("pdf"))
#         self._template.configure(template_data)
#         self._try_gen_synth_data_for_template_instance()

#     def _try_gen_synth_data_for_template_instance(self):
#         num_trials_per_doc = 3
#         for num_trial in range(1, num_trials_per_doc + 1):
#             try:
#                 self._gen_synth_data_for_template_instance()
#                 return
#             except Exception as e:
#                 if (num_trial == num_trials_per_doc): raise e

#     def _handle_latex_files_generation_exception(self, exception):
#         self._logger.log_error_creating_doc_instance_for_template(
#             self._organization_data.get_template_instance_num())
#         self._logger.log_latex_file_gen_exception(
#             self._organization_data.get_gen_file_name(),
#             self._organization_data.get_template_name(),
#             exception)
#         self._cleanup_all_generated_files()

#     def _cleanup_all_generated_files(self):
#         FileCleaner().cleanup_files(
#             self._gen_instance_file_storage_path(), ignore_config=True)

#     def _gen_synth_data_for_template_instance(self):
#         """
#         Generates the synthetic pdf document alongside its ground truth values.
#         The generated data is stored as a .json file (that entails all the GT
#         values) and .png images (the document pages).
#         """
#         print('creating document')
#         doc = DocumentCreator().create_doc()
#         print(f'created document with Document Creator')

#         #generate the PDF,aux, log, pow, pwpows, tex and trpos files
#         self._gen_files_from_doc(doc)
#         doc_file_path = self._gen_instance_file_storage_path("pdf")
#         file_done = os.path.isfile(doc_file_path)

#         #check if the files were creating correctly before going into the next one
#         if file_done:  
#             print(f'exportin gen data from files')
#             #obtain all the bounding box informations needed for refinement
#             doc_export_data = self._gen_export_data_from_files()
#             print(f'get final synth doc pdf file')
#             #add watermark (bounding box would fail if watermark was be added before)
#             self._gen_final_synth_doc_pdf_file(doc)
#             # print(f'add page images')
#             # doc_export_data.add_page_images()
#             try:
#                 doc_export_data.dump()
#             except:
#                 print('Dumped Except')

#         self._cleanup_temp_compilation_files()
#         self._logger.log_created_doc_instance_for_template(
#             self._organization_data.get_template_instance_num())

#     def _gen_files_from_doc(self, doc):
#         # Must compile twice to use updated logged position values.
#         self._compile_files(doc)
#         self._compile_files(doc)
#         self._compile_files(doc)

#     def _gen_export_data_from_files(self) -> DocumentExportData:
#         #path for the calculated positions of the elements in the syn file
#         pos_log_file_path = self._gen_instance_file_storage_path("pos")
#         #path where the syn pdf are going to be saved in
#         doc_file_path = self._gen_instance_file_storage_path("pdf")
#         #return a DocumentExportData, class used to transform (for example)
#         #the current latex document into images
#         return WritePosLogsToJsonSerializer().log_file_to_export_data(
#             pos_log_file_path, doc_file_path)

#     def _gen_final_synth_doc_pdf_file(self, doc: CustomDocument):
#         is_data_added = doc.add_data_post_position_log_compilation()
#         if (is_data_added):
#             self._compile_files(doc)

#     def _compile_files(self, doc):
#         # try:
#         print("compiling doc")
#         # print("--:",doc)
#         print("#########################")
#         try:
#             doc.generate_pdf(
#                 self._gen_instance_file_storage_path(),
#                 clean=self._config.clean_non_pdf_files(),
#                 clean_tex=self._config.clean_tex_files(),
#                 compiler="lualatex")
#             print('done compiling the pdf files')
#         except Exception as e:
#             print(f'errror {e}')

#     def _cleanup_temp_compilation_files(self):
#         FileCleaner().cleanup_files(self._gen_instance_file_storage_path())

#     def _gen_instance_file_storage_path(self, extension: str=None):
#         ext = "" if (extension is None) else f".{extension}"
#         files_storage_path = self._organization_data.get_gen_files_storage_path()
#         template_name = self._organization_data.get_template_name()
#         instance_num = self._organization_data.get_template_instance_num()
#         return (f"{files_storage_path}_{template_name.replace('-', '_')}_"
#             f"{instance_num}{ext}")

# class OrganizationData:

#     def __init__(self):
#         self._files_storage_path = None
#         self._template_name = None
#         self._template_instance_num = None

#     def get_gen_files_storage_path(self) -> str:
#         return self._files_storage_path

#     def get_gen_file_name(self) -> str:
#         return file_path_manager.extract_fname_wo_ext(self._files_storage_path)

#     def get_template_name(self) -> str:
#         return self._template_name

#     def get_template_instance_num(self) -> int:
#         return self._template_instance_num

#     def set_gen_files_storage_path(self, files_storage_path: str):
#         self._files_storage_path = files_storage_path

#     def set_template_name(self, template_name: str):
#         self._template_name = template_name

#     def set_template_instance_num(self, template_instance_num: int):
#         self._template_instance_num = template_instance_num

# def parse_cmd_line_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(description="Synthetic Data Generator")
#     parser.add_argument("-e", "--env", default="dev",
#         help="Environment: 'dev' or 'production'")
#     parser.add_argument("-c", "--config", required=True,
#         help="Path to the configuration JSON file")
#     parser.add_argument("-w", "--workers", type=int, default=os.cpu_count(),
#         help="Number of parallel workers (default: number of CPU cores)")

#     return parser.parse_args()

# def filter_documents_without_tables(documents: list):
#     import json
#     documents_with_tables = []
#     base_path = 'synthetic_data_generation/dataset/demo/chinese'
#     for document in documents:
#         json_path = os.path.join(base_path, document)
#         try:
#             with open(json_path, 'r') as file:
#                 data = json.load(file)
#             if len(data['tables']) > 3:
#                 documents_with_tables.append(document)
#         except:
#             pass
#     print(f'seed documents with tables {len(documents_with_tables)}')
#     return documents_with_tables

# def main(cmd_line_args: argparse.Namespace):
#     config = Config(config_file_path=cmd_line_args.config)
#     generator = SyntheticDataGenerator(cmd_line_args, config)
#     generator.gen_dataset()

# if "__main__" == __name__:
#     main(parse_cmd_line_args())

import argparse
import sys

sys.path.append('synthetic_data_generation/chart_rendering/src')

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
from datetime import datetime

import os
import json
from multiprocessing import Pool
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
        print(f"Dataset path: {self.dataset_path}")
        self._template = Template()
        self._data_stores_manager = DataStoresManager()
        self._logger = Logger()
        self._organization_data = OrganizationData()
        
        # Load the config JSON to read document selection
        self._config_data = self._load_config_json()
        
        # Determine which files to process based on config
        self._selected_doc_file_names = self._determine_files_to_process()
        
        print(f"Selected {len(self._selected_doc_file_names)} files for processing:")
        for i, filename in enumerate(self._selected_doc_file_names):
            print(f"  {i+1}. {filename}")

    def _load_config_json(self):
        """Load the configuration JSON file"""
        try:
            with open(self._cmd_line_args.config, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config file: {e}")
            return {}

    def _determine_files_to_process(self):
        """
        Determine which files to process based on config JSON document-selection
        """
        document_selection = self._config_data.get('document-selection', {})
        
        # Priority 1: Check for "all" selection
        if 'all' in document_selection:
            print("Processing all files (from config: document-selection.all)")
            return self._get_all_files()
        
        # Priority 2: Check for "custom" selection with specific file names
        if 'custom' in document_selection:
            custom_config = document_selection['custom']
            if 'document-file-names' in custom_config:
                file_names = custom_config['document-file-names']
                print(f"Processing custom files from config: {file_names}")
                return self._get_custom_files(file_names)
        
        # Priority 3: Legacy - Config file selection (existing method)
        config_selected_files = self._config.get_selected_doc_file_names()
        if config_selected_files:
            print("Using files from legacy config method")
            return config_selected_files
        
        # Priority 4: Default behavior with start/finish indices
        print("Using default behavior with start/finish indices")
        return self._get_files_by_indices()
    
    def _get_all_files(self):
        """Get all files in the dataset directory"""
        all_files = [f for f in os.listdir(self.dataset_path) 
                    if os.path.isfile(os.path.join(self.dataset_path, f))]
        all_files.sort()
        return all_files
    
    def _get_custom_files(self, file_names):
        """Get specific files from the list, validate they exist"""
        validated_files = []
        for filename in file_names:
            file_path = os.path.join(self.dataset_path, filename)
            if os.path.isfile(file_path):
                validated_files.append(filename)
                print(f"  ✓ Found: {filename}")
            else:
                print(f"  ✗ Warning: File '{filename}' not found in dataset directory: {self.dataset_path}")
        
        if not validated_files:
            raise FileNotFoundError(f"None of the specified files were found in dataset directory: {self.dataset_path}")
        
        return validated_files
    
    def _get_files_by_indices(self):
        """Get files based on start and finish indices from config"""
        all_files = self._get_all_files()
        
        start_index = self._config.get_doc_start_index()
        finish_index = self._config.get_doc_finish_index()
        
        print("start index: ", start_index)
        print("finish_index: ", finish_index)
        
        # Update finish_index if it's beyond the number of files
        total_files = len(all_files)
        if finish_index >= total_files:
            finish_index = total_files - 1  # -1 because indices are 0-based
            print(f"Adjusted finish_index to {finish_index} (total files: {total_files})")
        
        # Slice the files from start_index to finish_index (inclusive)
        selected_files = all_files[start_index:finish_index + 1]
        print(f"Selected {len(selected_files)} files from index {start_index} to {finish_index}")
        
        return selected_files

    def gen_dataset(self):
        """
        Generate dataset using parallel processing for multiple documents
        """
        self._logger.log_program_start()
        
        # Create tuples of (index, doc_file_name) for parallel processing
        index_doc_file_name_tuples = list(enumerate(self._selected_doc_file_names, start=1))
        
        num_cores = self._cmd_line_args.workers
        print(f"Processing {len(index_doc_file_name_tuples)} documents using {num_cores} workers")
        
        # Use multiprocessing to process documents in parallel
        with Pool(processes=num_cores) as pool:
            # Use tqdm for progress tracking (note: progress updates may not be perfectly accurate due to parallel processing)
            list(tqdm(
                pool.imap(self._gen_dataset_for_doc_wrapper, index_doc_file_name_tuples),
                total=len(index_doc_file_name_tuples),
                desc="Processing documents"
            ))
        
        # Log completion
        start_index = 1
        finish_index = len(self._selected_doc_file_names)
        self._logger.log_program_end()

    def _gen_dataset_for_doc_wrapper(self, doc_tuple: tuple):
        """
        Wrapper method for parallel processing
        """
        return self.gen_dataset_for_doc(doc_tuple)

    def gen_dataset_for_doc(self, doc_tuple: tuple):
        doc_index = doc_tuple[0]
        doc_file_name = doc_tuple[1]
        self._logger.log_creating_dataset_for_doc(doc_index, doc_file_name)
        doc_file_path = self._config.gen_doc_file_path(doc_file_name)
        self._data_stores_manager.init_doc_data_stores(doc_file_path)
        template_creation_infos = (self._config.
            get_selected_template_creation_infos())
        for template_creation_info in template_creation_infos:
            try:
                print(f'template info {template_creation_info.get_template_data()}')
                self._organization_data.set_gen_files_storage_path(
                    self._config.gen_gen_files_storage_path(
                        doc_file_path, template_creation_info.get_template_type()))
                self._organization_data.set_template_name(
                    template_creation_info.get_template_name())
                self._gen_dataset_for_template(template_creation_info)
            except Exception as e:
                print(f'skipping document for {e}')
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
        print('creating document')
        doc = DocumentCreator().create_doc()
        print(f'created document with Document Creator')

        #generate the PDF,aux, log, pow, pwpows, tex and trpos files
        self._gen_files_from_doc(doc)
        doc_file_path = self._gen_instance_file_storage_path("pdf")
        file_done = os.path.isfile(doc_file_path)

        #check if the files were creating correctly before going into the next one
        if file_done:  
            print(f'exportin gen data from files')
            #obtain all the bounding box informations needed for refinement
            doc_export_data = self._gen_export_data_from_files()
            print(f'get final synth doc pdf file')
            #add watermark (bounding box would fail if watermark was be added before)
            self._gen_final_synth_doc_pdf_file(doc)
            # print(f'add page images')
            # doc_export_data.add_page_images()
            try:
                doc_export_data.dump()
            except:
                print('Dumped Except')

        self._cleanup_temp_compilation_files()
        self._logger.log_created_doc_instance_for_template(
            self._organization_data.get_template_instance_num())

    def _gen_files_from_doc(self, doc):
        # Must compile twice to use updated logged position values.
        self._compile_files(doc)
        self._compile_files(doc)
        self._compile_files(doc)

    def _gen_export_data_from_files(self) -> DocumentExportData:
        #path for the calculated positions of the elements in the syn file
        pos_log_file_path = self._gen_instance_file_storage_path("pos")
        #path where the syn pdf are going to be saved in
        doc_file_path = self._gen_instance_file_storage_path("pdf")
        #return a DocumentExportData, class used to transform (for example)
        #the current latex document into images
        return WritePosLogsToJsonSerializer().log_file_to_export_data(
            pos_log_file_path, doc_file_path)

    def _gen_final_synth_doc_pdf_file(self, doc: CustomDocument):
        is_data_added = doc.add_data_post_position_log_compilation()
        if (is_data_added):
            self._compile_files(doc)

    def _compile_files(self, doc):
        # try:
        print("compiling doc")
        # print("--:",doc)
        print("#########################")
        try:
            doc.generate_pdf(
                self._gen_instance_file_storage_path(),
                clean=self._config.clean_non_pdf_files(),
                clean_tex=self._config.clean_tex_files(),
                compiler="lualatex")
            print('done compiling the pdf files')
        except Exception as e:
            print(f'errror {e}')

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
    parser.add_argument("-w", "--workers", type=int, default=os.cpu_count(),
        help="Number of parallel workers (default: number of CPU cores)")

    return parser.parse_args()

def filter_documents_without_tables(documents: list):
    import json
    documents_with_tables = []
    base_path = 'synthetic_data_generation/dataset/demo/chinese'
    for document in documents:
        json_path = os.path.join(base_path, document)
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
            if len(data['tables']) > 3:
                documents_with_tables.append(document)
        except:
            pass
    print(f'seed documents with tables {len(documents_with_tables)}')
    return documents_with_tables

def main(cmd_line_args: argparse.Namespace):
    config = Config(config_file_path=cmd_line_args.config)
    generator = SyntheticDataGenerator(cmd_line_args, config)
    generator.gen_dataset()

if __name__ == "__main__":
    main(parse_cmd_line_args())