from .stack import Stack

class SectionStack(Stack):

    def __init__(self):
        super().__init__()

    def get_active_section(self):
        return self.top()

    def get_active_section_type(self):
        return type(self.top())

    def set_active_section(self, section):
        self.pop_lower_level_sections(section)
        self.pop_same_level_section(section)
        self.push(section)

    def pop_lower_level_sections(self, section):
        while ((self.has_items()) and (type(self.top()) != type(section))):
            self.pop()

    def pop_same_level_section(self, section):
        if ((self.has_items()) and (type(self.top()) == type(section))):
            self.pop()
