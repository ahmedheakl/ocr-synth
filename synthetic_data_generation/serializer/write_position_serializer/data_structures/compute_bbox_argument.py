from .log_line_data import LogLineData

class ComputeBboxArgument:

    def __init__(
        self,
        start_log_line: LogLineData,
        end_log_line: LogLineData,
        page_num: int
    ):
        self.sll = start_log_line
        self.ell = end_log_line
        self.page_num = page_num
