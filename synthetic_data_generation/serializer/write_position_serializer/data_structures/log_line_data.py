import re

class LogLineData:

    def __init__(self, log_file_line: str):
        # Position units are stored in sp (latex default).
        pos_data = PosData(log_file_line)
        self.page_num = pos_data.page_num
        self.xpos = pos_data.xpos
        self.ypos = pos_data.ypos
        self.data_item_index = self._extract_data_item_index(log_file_line)
        print(f"log line data {self.data_item_index}")
        self.is_start_log_line = self._check_is_start_log_line(log_file_line)

    def is_on_even_page(self):
        return not self.is_on_odd_page()

    def is_on_odd_page(self):
        return self.page_num % 2 != 0

    def to_str(self):
        start_end_identifier = "s" if (self.is_start_log_line) else "e"
        index = f"{start_end_identifier}pos{self.data_item_index}"
        position = f"{self.xpos},{self.ypos},{self.page_num}"
        return index + ":" + position

    def _extract_data_item_index(self, log_file_name):
        identifier = log_file_name.split(":")[0]
        item_index = int(identifier[4:])
        return item_index

    def _check_is_start_log_line(self, log_file_line):
        identifier = log_file_line[0]
        return identifier == "s"

    def __str__(self):
        return (
            "----- Log Line Data -----\n"
            f"page num = {self.page_num}\n"
            f"xpos     = {self.xpos}\n"
            f"ypos     = {self.ypos}\n"
            f"data item index = {self.data_item_index}"
            "-------------------------")


class PosData:

    def __init__(self, log_file_line: str):
        pos_data_csv = log_file_line.split(":")[-1]
        pos_data_list = pos_data_csv.split(',')

        self.xpos = int(pos_data_list[0])
        self.ypos = int(pos_data_list[1])

        # Sanitize the page number by removing non-digit characters
        raw_page = pos_data_list[2].strip()
        cleaned_page = re.sub(r'[^\d]', '', raw_page)

        if not cleaned_page:
            raise ValueError(f"Cannot extract valid page number from: {raw_page}")

        self.page_num = int(cleaned_page)