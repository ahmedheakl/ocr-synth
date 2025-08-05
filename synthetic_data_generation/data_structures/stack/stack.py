class Stack:

    def __init__(self):
        self._size = 0
        self._items = []

    def push(self, section):
        self._items.append(section)
        self._size += 1

    def pop(self):
        self._size -= 1
        return self._items.pop()

    def top(self):
        return self._items[-1]

    def get_size(self):
        return self._size

    def has_items(self):
        return not self.is_empty()

    def is_empty(self):
        return self._size == 0
