from .prov_item import ProvItem

class Prov:

    def __init__(self, prov: list):
        self._items = [ProvItem(item) for item in prov]

    def get_first_item(self):
        return self._items[0]

    def get_item(self, index: int):
        return self._items[index]

    def get_items(self):
        return self._items

    def get_items_sorted_by_page_num(self) -> dict[int:[ProvItem]]:
        prov_items_sorted = {}
        for prov_item in self._items:
            if (prov_item.get_page_num()) in prov_items_sorted:
                prov_items_sorted[prov_item.get_page_num()].append(prov_item)
            else:
                prov_items_sorted[prov_item.get_page_num()] = [prov_item]
        return prov_items_sorted

    def get_num_items(self):
        return len(self._items)

    def are_items_spread_across_pages(self):
        init_page = self._items[0].get_page_num()
        for item in self._items:
            if (init_page != item.get_page_num()):
                return True
        return False

    def extend(self, items: list):
        self._items += items

    def pop(self, index):
        self._items.pop(index)

    def to_list_of_dicts(self):
        return [item.to_dict() for item in self._items]
