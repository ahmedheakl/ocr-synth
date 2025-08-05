class FileGenException:

    def __init__(self, file_name: str, template_name: str, exception):
        self._file_name = file_name
        self._template_name = template_name
        self._exception = exception

    def get_file_name(self) -> str:
        return self._file_name

    def get_template_name(self) -> str:
        return self._template_name

    def get_exception(self):
        return self._exception

class Logger:

    def __init__(self):
        self._latex_file_gen_exceptions = []

    def log_program_start(self):
        print("Creating latex dataset ...")

    def log_program_end(self):
        print("Finished creating latex dataset.")

    def log_creating_dataset_for_doc(self, doc_index: int, doc_name: str):
        self.print_big_separator()
        print(f"Creating dataset for document: {doc_name} (Index: {doc_index})")
        self.print_small_separator()

    def log_created_dataset_for_doc(self):
        self.print_small_separator()
        print("Created dataset for document!")
        self.print_big_separator()

    def log_creating_doc_instances_for_template(
        self, template_name: str, num_template_instances: int
    ):
        print(f">> Creating {num_template_instances} instances for template: "
            f"{template_name}")

    def log_created_doc_instances_for_template(self):
        print(">> Finished creating template instances!")

    def log_created_doc_instance_for_template(self, instance_num: int):
        print(f">>>> Created instance: {instance_num}")

    def log_error_creating_doc_instance_for_template(self, instance_num: int):
        print(f">>>> [ERROR] Failed to create instance: {instance_num}")

    def log_latex_file_gen_exception(
        self, file_name: str, template_name: str, exception
    ):
        self._latex_file_gen_exceptions.append(
            FileGenException(file_name, template_name, exception))

    def log_latex_file_generation_errors_to_file(
        self, doc_start_index: int, doc_end_index: int
    ):
        file_path = ("synthetic_data_generation/logging/logs/"
            "latex_file_generation_error_logs_doc_indexes_"
            f"{doc_start_index}_to_{doc_end_index}.txt")
        with open(file_path, "w") as file_pointer:
            if (len(self._latex_file_gen_exceptions) == 0):
                file_pointer.write("Latex files created without errors!")
            else:
                self._write_exceptions_to_log_file(file_pointer)                

    def _write_exceptions_to_log_file(self, file_pointer):
        for exception in self._latex_file_gen_exceptions:
            file_pointer.write(self._gen_log_file_message(exception))

    def _gen_log_file_message(self, file_gen_exception: FileGenException):
        return ("======================================================\n"
                f"File    : {file_gen_exception.get_file_name()}\n"
                f"Template: {file_gen_exception.get_template_name()}\n"
                "Exception: "
                f"{file_gen_exception.get_exception()}\n\n")

    def print_big_separator(self):
        print("============================================")

    def print_small_separator(self):
        print("--------------------------------------------")
