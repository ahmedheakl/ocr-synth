import time
import copy 

class DoclingDataStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DoclingDataStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._data = {}
        self._initialized = True

    def set_data(self, data: dict):
        self._data = data

    def get_data(self) -> dict:
        return self._data

    # New method: get_document returns the entire data dict.
    def get_document(self) -> dict:
        return self._data

    # Accessors for top-level keys
    def get_schema_name(self) -> str:
        return self._data.get("schema_name", "")
    
    def get_version(self) -> str:
        return self._data.get("version", "")

    def get_name(self) -> str:
        return self._data.get("name", "")

    def get_origin(self) -> dict:
        return self._data.get("origin", {})
    
    def get_file_hash(self) -> str:
        return str(self.get_origin().get('binary_hash', 0))
    
    def get_file_name(self)-> str:
        return self.get_origin().get('filename', 'not_found').split('.')[0]

    def get_furniture(self) -> dict:
        return self._data.get("furniture", {})

    def get_body(self) -> dict:
        return self._data.get("body", {})

    def get_groups(self) -> list:
        return self._data.get("groups", [])

    def get_texts(self) -> list:
        return self._data.get("texts", [])
    
    def get_tables(self) -> list:
        return self._data.get("tables", [])
    
    def get_pages_pixel_dimension(self) -> tuple:
        h = self._data['pages']['1']['size'].get('height', 0)
        w = self._data['pages']['1']['size'].get('width', 0)
        return h, w
    
    #New method, list of all the components in the document
    def get_main_text(self) -> list:
        body = self._data.get("body", {}).get("children", [])
        len_body = len(body)
        texts = copy.deepcopy(self.get_texts())
        len_texts = len(texts)
        pictures = copy.deepcopy(self.get_pictures())
        len_pictures = len(pictures)
        tables = self.get_tables()
        groups = self.get_groups()
        main_text = []
        for i, child in enumerate(body):
            ref = child.get('$ref', "").split('/')
            ref_type = ref[1]
            ref_number = int(ref[2])
            if 'text' in ref_type:
                # child_to_add = texts[ref_number]
                # main_text.append(child_to_add)
                self._recursive_append(child['$ref'], main_text, texts, pictures, groups, tables)
            elif 'picture' in ref_type:
                child_to_add = pictures[ref_number]
                main_text.append(child_to_add)
            elif 'tables' in ref_type:
                child_to_add = tables[ref_number]
                main_text.append(child_to_add)
            elif 'groups' in ref_type:
                #for now only support list groups
                # child_to_add = groups[ref_number]
                # if child_to_add['label'] == 'list':
                #     main_text.append(child_to_add)
                self._recursive_append(child['$ref'], main_text, texts, pictures, groups, tables)
            else:
                print('label not found')
        return main_text
    
    def _recursive_append(self, element, main_text: list, texts, pictures, groups, tables):
        '''The docling document is defined as a tree, I need to explore all the different branches
            until I find the leaves. This operation will be done recursively and append to main_text'''
        child_to_add = self._retrieve_component_by_reference_no_storage(element, texts, pictures, groups, tables)
        childrens_dict = child_to_add.get('children', [])
        childrens = [child['$ref'] for child in childrens_dict]
        ref = element.split('/')
        ref_type = ref[1]
        ref_number = int(ref[2])
        if 'text' in ref_type:
            child_to_add = texts[ref_number]
            main_text.append(child_to_add)
            if len(childrens) > 0:
                for child in childrens:
                    self._recursive_append(child, main_text, texts, pictures, groups, tables)
        elif 'picture' in ref_type:
            child_to_add = pictures[ref_number]
            main_text.append(child_to_add)
        elif 'tables' in ref_type:
            child_to_add = tables[ref_number]
            main_text.append(child_to_add)
        elif 'groups' in ref_type:
            #for now only support list groups
            child_to_add = groups[ref_number]
            if child_to_add['label'] == 'list' or child_to_add['label'] == 'inline':
                main_text.append(child_to_add)
                return
            else:
                if len(childrens) > 0:
                    for child in childrens:
                        self._recursive_append(child, main_text, texts, pictures, groups, tables)

        else:
            print('label not found')
    
    def _retrieve_component_by_reference_no_storage(self, reference: str, texts, pictures, groups, tables):
        reference_split = reference.split('/')
        reference_type = reference_split[1]
        reference_index = int(reference_split[2])
        if reference_type == 'texts':
            return texts[reference_index]
        elif reference_type == 'pictures':
            return pictures[reference_index]
        elif reference_type == 'tables':
            return tables[reference_index]
        elif reference_type == 'groups':
            return groups[reference_index]
        else:
            return None
     
    def get_group_children(self, group_ref: str):
        texts = self.get_texts()
        pictures = self.get_pictures()
        tables = self.get_tables()
        groups = self.get_groups()
        group = self._retrieve_component_by_reference_no_storage(group_ref, texts, pictures, groups, tables)
        children_ref = [child['$ref'] for child in group['children']]
        children = []
        for child_ref in children_ref:
            children.append(self._retrieve_component_by_reference_no_storage(child_ref, texts, pictures, groups, tables))
        return children

    def get_pictures(self) -> list:
        return self._data.get("pictures", [])

    # Example helper to get a specific text item by index
    def get_text_by_index(self, index: int) -> dict:
        texts = self.get_texts()
        if 0 <= index < len(texts):
            return texts[index]
        return None

    # New helper: get_main_text_item returns the text item at the given index.
    def get_main_text_item(self, index: int) -> dict:
        texts = self.get_texts()
        if 0 <= index < len(texts):
            return texts[index]
        return None

    # Example helper to get a specific picture by index
    def get_picture_by_index(self, index: int) -> dict:
        pics = self.get_pictures()
        if 0 <= index < len(pics):
            return pics[index]
        return None

    # Additional getter: get children of the body.
    def get_body_children(self) -> list:
        body = self.get_body()
        return body.get("children", [])

    def clear(self):
        self._data = {}
