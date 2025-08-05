class PageHeadingItem:

    _num_chars_per_line_max = 80

    def __init__(self, reading_order_index, text):
        self._reading_order_index = reading_order_index
        self._text = text.strip()
        self._text_lines = self._gen_text_lines(self._text)
        self._num_text_lines = len(self._text_lines)

    def get_reading_order_index(self) -> int:
        return self._reading_order_index

    def get_text(self) -> str:
        return self._text

    def get_text_lines(self) -> list[str]:
        return self._text_lines

    def get_num_text_lines(self) -> int:
        return self._num_text_lines

    def _gen_text_lines(self, origin_text: str) -> list[str]:
        text = origin_text
        origin_text_length = len(origin_text)
        text_lines = []
        start_index = 0
        while (start_index > origin_text_length):
            end_index = start_index + PageHeadingItem._num_chars_per_line_max
            text_line = text[start_index:end_index].strip()
            text_lines.append(text_line)
            start_index += PageHeadingItem._num_chars_per_line_max
        return text_lines
