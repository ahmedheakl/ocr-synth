class ParagraphItemPositions:
    """
    Stores the text data of a paragraph main text item. The paragraph is split
    into substrings which are stored according to the page and the specific
    column on that page they belong to.
    """

    def __init__(self, mti_index: int):
        self._mti_index = mti_index
        #self._data contains all the words of a paragraph, grouped based on
        #the column and the page number into substrings.
        
        '''
        Example:
        <document>
        riga111     riga121
        riga112     riga122
        riga113     riga123

        <page break>

        riga211     riga221
        riga212     riga222
        riga213     riga223
        <document>
        self._data would be: {'0': 
                                    {'0': "riga111\nriga112\riga113",
                                     '1': "riga121\nriga122\nriga123"}
                              '1': 
                                    ....
                            }
        '''
        self._data = {} # {<page_num>: {<col_index>: SubstringItem, ...}, ...}
        self.first_word_y = 0

    def get_substring(self, page_num: int, page_col_index: int) -> str:
        print('current self data')
        if page_num in self._data.keys():
            print(f'asking for column number {page_col_index}')
            print(f'columns in page {page_num} {list(self._data[page_num].keys())}')
        substring_item = self._data[page_num][page_col_index]
        return substring_item.get_string()

    def has_text_break(self, page_num: int, page_col_index: int) -> bool:
        substring_item = self._data[page_num][page_col_index]
        return substring_item.has_text_break()

    # def has_text_break(self, page_num: int, page_col_index: int) -> bool:
    #     # OLD: substring_item = self._data[page_num][page_col_index]
        
    #     # NEW: Safe access with fallback
    #     if page_num in self._data and page_col_index in self._data[page_num]:
    #         substring_item = self._data[page_num][page_col_index]
    #     else:
    #         # Use first available column as fallback
    #         available_cols = list(self._data[page_num].keys()) if page_num in self._data else []
    #         if available_cols:
    #             substring_item = self._data[page_num][available_cols[0]]
    #         else:
    #             print("i did not work")
    #             return False
        
    #     return substring_item.has_text_break()

    def has_page_break(self, page_num: int, page_col_index: int) -> bool:
        substring_item = self._data[page_num][page_col_index]
        return substring_item.has_page_break()

    def add_word_to_substring(
        self, page_num: int, col_index: int, word: str
    ) -> str:
        if (page_num in self._data):
            self._update_page_item(page_num, col_index, word)
        else:
            self._create_page_item(page_num, col_index, word)

    def _update_page_item(self, page_num: int, col_index: int, word: str):
        col_index_max = max(self._data[page_num].keys())
        if (col_index > col_index_max):
            self._add_text_break()
            self._data[page_num][col_index] = SubstringItem(word)
        else:
            substring_item = self._data[page_num][col_index_max]
            substring_item.add_word(word)

    def _add_text_break(self):
        last_page_index = max(self._data.keys())
        last_col_index = max(self._data[last_page_index])
        substring_item = self._data[last_page_index][last_col_index]
        substring_item.set_text_break()

    def _create_page_item(self, page_num: int, col_index: int, word: str):
        self._add_page_break()
        self._data[page_num] = {col_index: SubstringItem(word)}

    def _add_page_break(self):
        if (self._has_page_entries()):
            prev_page_index = max(self._data.keys())
            last_col_index = max(self._data[prev_page_index])
            substring_item = self._data[prev_page_index][last_col_index]
            substring_item.set_page_break()

    def _has_page_entries(self) -> bool:
        return (len(self._data.keys()) > 0)
    
    def set_first_word_y(self, y: int):
        self.first_word_y = y

    def get_first_word_y(self):
        return self.first_word_y

class SubstringItem:

    def __init__(self, string: str):
        self._substring = string
        self._has_text_break = False
        self._has_page_break = False

    def get_string(self) -> str:
        return self._substring

    def has_text_break(self) -> bool:
        return self._has_text_break

    def has_page_break(self) -> bool:
        return self._has_page_break

    def add_word(self, word: str):
        self._substring += " " + word

    def set_text_break(self):
        self._has_text_break = True

    def set_page_break(self):
        self._has_page_break = True
