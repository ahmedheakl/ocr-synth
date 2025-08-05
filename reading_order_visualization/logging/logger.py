class FileGenException:

    def __init__(self, file_name, exception):
        self.file_name = file_name
        self.exception = exception

class Logger:

    def __init__(self):
        self._latex_vis_gen_exceptions = []

    def log_info_program_start(self):
        print("Creating visualization files ...")

    def log_info_program_end(self):
        print("Finished creating visualization files.")

    def log_info_created_vis_for_latex_file(self, file_name: str):
        print(f"[SUCCESS] Generated vis for: {file_name}")

    def log_error_failed_to_create_vis_for_latex_file(self, file_name: str):
        print(f"[ERROR] Vis file generation failed for: {file_name}")

    def log_vis_file_gen_exception(self, file_name: str, exception):
        file_gen_exception = FileGenException(file_name, exception)
        self._latex_vis_gen_exceptions.append(file_gen_exception)

    def log_vis_file_generation_errors_to_file(self):
        file_path = ("reading_order_visualization/logging/logs/" +
                     "vis_file_generation_error_logs.txt")
        with open(file_path, "w") as file_pointer:
            if (len(self._latex_vis_gen_exceptions) == 0):
                file_pointer.write("Vis files created without errors!")
            else:
                self._write_exceptions_to_log_file(file_pointer)

    def _write_exceptions_to_log_file(self, file_pointer):
        for exception in self._latex_vis_gen_exceptions:
            file_pointer.write(self._gen_log_file_message(exception))

    def _gen_log_file_message(self, file_gen_exception: FileGenException):
        return ("======================================================\n"
                f"File name: {file_gen_exception.file_name}\n"
                "Exception:\n"
                f"{file_gen_exception.exception}\n\n")
