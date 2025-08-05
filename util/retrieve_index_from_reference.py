from util.data_stores.docling_data_store import DoclingDataStore

def retrieve_index_from_reference(data: dict):
    """In docling each item has a self ref
    made by #/ref_type_/ref_index"""
    try:
        reference = data['self_ref'].split('/')
        return int(reference[2])
    except:
        return None

def retrieve_index_type_from_reference_string(ref: str):
    """In docling each item has a self ref
    made by #/ref_type_/ref_index"""
    try:
        reference = ref.split('/')
        return int(reference[2]), reference[1]
    except:
        return None
    
def retrieve_component_from_index_and_type(index: int, type: str):
    data_store = DoclingDataStore()
    if type == 'texts':
        texts = data_store.get_texts()
        return texts[index]
    elif type == 'pictures':
        pictures = data_store.get_pictures()
        return pictures[index]
    elif type == 'tables':
        tables = data_store.get_tables()
        return tables[index]
    elif type == 'groups':
        groups = data_store.get_groups()
        return groups[index]
    else:
        return None