class LatexCompilationExceptionHandler:

    def __init__(self):
        self._exception_msg_identifiers = [
            "Command '['xelatex'",
            "'utf-8' codec can't"
        ]

    def handle_compilation_exception(self, exception):
        if (self._is_unconcerning_pylatex_exception(exception)): return
        raise exception

    def _is_unconcerning_pylatex_exception(self, exception):
        for identifier in self._exception_msg_identifiers:
            if (identifier in str(exception)):
                return True
        return False
