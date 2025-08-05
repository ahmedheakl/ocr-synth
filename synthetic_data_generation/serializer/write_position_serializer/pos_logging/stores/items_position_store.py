

class ItemsPositionStore:

    def __init__(self):
        self._items = {} # {main_item_index: <data>, ...}

    def get_item_positions(self, index: int):
        if (index in self._items):
            return self._items[index]
        return None
