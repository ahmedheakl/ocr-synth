def get_item_ref_index(item: dict) -> int:
    possible_ref_keys = [
        "__ref",
        "$ref"
    ]
    for possible_ref_key in possible_ref_keys:
        if (possible_ref_key in item):
            ref = item[possible_ref_key]
            index = int(ref.split("/")[-1])
            return index
    return None

def get_item_text(item: dict) -> str:
    if ("text" in item):
        return item["text"]
    return None
