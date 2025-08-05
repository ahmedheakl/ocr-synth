import json

from synthetic_data_generation.templates.template import Template
from .ground_truth_item import GroundTruthItem
from util.retrieve_index_from_reference import retrieve_index_type_from_reference_string
from copy import deepcopy
import hashlib

class GroundTruthData:

    def __init__(self):
        self._data = {}

    def get_indexes(self, is_sorted=False) -> list[int]:
        if (is_sorted):
            return sorted(self._data)
        return list(self._data.keys())

    def get_data(self):
        return self._data.values()

    def get_item(self, index):
        if (index in self._data):
            return self._data[index]
        return None

    def add_with_overwrite_existing_item(self, item: GroundTruthItem):
        self._data[item.get_index()] = item

    def add_with_append_to_existing_item(self, item: GroundTruthItem):
        item_index = item.get_index()
        if (item_index in self._data):
            self._data[item_index].append(item)
        else:
            self._data[item_index] = item

    def to_export_format(self):
        for key in sorted(self._data):
            gt_item = self._data[key]
            gt_item.to_export_format()

    def gen_visualization_json_file(self, dir_path, file_name, pos_store):
        file_path, file_name = self._gen_vis_json_file_path(dir_path, file_name)
        json_data = self._gen_vis_data(pos_store)
        json_data['name'] = file_name
        hash_object = hashlib.sha256(file_name.encode())
        with open(file_path, "w") as fp:
            json.dump(json_data, fp, indent=2)

    def _gen_vis_json_file_path(self, dir_path, file_name):
        file_name_wo_ext = file_name.split(".")[0]
        full_file_name = file_name_wo_ext + ".json"
        return dir_path + full_file_name, file_name_wo_ext

    def _gen_vis_data(self, pos_store):
        json_data = self._gen_vis_json_skeleton()
        main_text = json_data["body"]['children']
        body_self_ref = json_data['body']['self_ref']
        texts = json_data['texts']
        pictures = json_data['pictures']
        tables = json_data['tables']
        groups = json_data['groups']

        pages = set()
        pages.add(1)

        inside_list_group = False
        for i, key in enumerate(sorted(self._data)):
            item = self._data[key]
            item_to_add = item.to_reading_order_format()[0]

            pos_element = pos_store.get_or_none_item(i)
            if pos_element is not None:
                try:
                    new_starting_y = pos_element.get_first_word_y()
                    if 'prov' in item_to_add.keys() and len(item_to_add['prov']) > 0 and 'section' not in item_to_add['label']:
                        if new_starting_y > item_to_add['prov'][0]['bbox']['b'] or new_starting_y < item_to_add['prov'][0]['bbox']['t']:
                            print(item_to_add['self_ref'])
                            print('label ', item_to_add['label'])
                            print('problem with bbox ')
                            print('text ', item_to_add['text'][:min(10, len(item_to_add['text']))])
                        else:
                            item_to_add['prov'][0]['bbox']['t'] = new_starting_y
                except Exception as e:
                    print('exception new y ', e)

            if 'prov' in item_to_add.keys() and len(item_to_add['prov']) > 0:
                for prov in item_to_add['prov']:
                    pages.add(prov['page_no'])

            item_to_add['parent']['$ref'] = body_self_ref
            ref_type = item_to_add.get('self_ref')
            index_type = '0'

            if inside_list_group and item_to_add['label'] != 'list_item':
                inside_list_group = False
                groups.append(list_group)

            if ref_type == 'texts':
                index_type = str(len(texts))
            elif ref_type == 'pictures':
                index_type = str(len(pictures))
            elif ref_type == 'tables':
                index_type = str(len(tables))
            elif ref_type == 'groups':
                index_type = str(len(groups))

            self_ref = '#/' + ref_type + '/' + index_type
            item_to_add['self_ref'] = self_ref

            # Attach caption logic
            children_refs = []
            caption_key = key + 1
            if caption_key in self._data:
                caption_item = self._data[caption_key].to_reading_order_format()[0]
                if caption_item.get("label") == "caption":
                    cap_ref_type = caption_item['self_ref']
                    cap_index = str(len(texts))
                    cap_ref = f"#/{cap_ref_type}/{cap_index}"
                    caption_item['self_ref'] = cap_ref
                    caption_item['parent']['$ref'] = self_ref
                    texts.append(caption_item)
                    children_refs.append({'$ref': cap_ref})
                    item_to_add['captions'] = [{'cref': cap_ref}]

            if ref_type == 'texts':
                if item_to_add['label'] == 'list_item':
                    if not inside_list_group:
                        inside_list_group = True
                        list_group = self._gen_list_group_skeleton()
                        list_group['children'].append({'$ref': self_ref})
                        list_group['parent']['$ref'] = body_self_ref
                        index_type_group = str(len(groups))
                        list_group_ref = '#/' + 'groups' + '/' + index_type_group
                        list_group['self_ref'] = list_group_ref
                        item_to_add['parent']['$ref'] = list_group_ref
                        main_text.append({'$ref':list_group_ref})
                    else:
                        list_group['children'].append({'$ref': self_ref})
                        item_to_add['parent']['$ref'] = list_group_ref
                    if i == len(sorted(self._data)) - 1:
                        inside_list_group = False
                        groups.append(list_group)
                else:
                    main_text.append({'$ref':self_ref})
                texts.append(item_to_add)
            elif ref_type == 'pictures':
                main_text.append({'$ref':self_ref})
                pictures.append(item_to_add)
            elif ref_type == 'tables':
                main_text.append({'$ref':self_ref})
                if children_refs:
                    item_to_add['children'] = children_refs
                tables.append(item_to_add)
            elif ref_type == 'groups':
                main_text.append({'$ref':self_ref})
                item_to_add.pop('prov', None)
                groups.append(item_to_add)

        json_data_page_1 = json_data['pages']['1']
        for pages_index in pages:
            if pages_index == 1:
                continue
            json_data_page_i = deepcopy(json_data_page_1)
            json_data_page_i['page_no'] = pages_index
            json_data['pages'][str(pages_index)] = json_data_page_i
        return json_data

    def _gen_list_group_skeleton(self):
        return {
            "self_ref": "",
            "parent": {'$ref': ""},
            'children': [],
            "content_layer": "furniture",
            "name": "group",
            "label": 'list',
        }

    def _gen_vis_json_skeleton(self):
        layout_settings = Template().get_layout_settings()
        return {
            "schema_name": "DoclingDocument",
            "version": "1.2.0",
            "name": "",
            "origin": {
                "mimetype": "application/pdf",
                "binary_hash": 0,
                "filename": ""
            },
            "furnitures": {},
            "body": {
                "self_ref": "#/body",
                "children": [],
                "content_layer": "body",
                "name": "_root_",
                "label": "unspecified"
            },
            "groups": [],
            "texts": [],
            "pictures": [],
            "tables": [],
            "key_value_items" : [],
            'form_items': [],
            "pages": {
                '1': {
                    'size': {
                        "width": layout_settings.get_page_width_px(),
                        "height": layout_settings.get_page_height_px()
                    },
                    'image': {
                        "mimetype": "image/png",
                        "dpi": 150,
                        "size": {
                            "width": 819.0,
                            "height": 1060.0
                        },
                        'uri': ''
                    },
                    'page_no': 1
                }
            }
        }