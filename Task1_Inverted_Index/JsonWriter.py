import json
import os

def create_json(inverted_index_dict):
    file_name = 'datamart.json'
    with open(file_name, 'w') as file:
        json.dump(inverted_index_dict, file)
        
    return None

def write_json(inverted_index_dict):
    file_name = 'datamart.json'

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            existing_data = json.load(file)
        existing_data.update(inverted_index_dict)

        with open(file_name, 'w') as file:
            json.dump(existing_data, file)
        
    else:
        create_json(inverted_index_dict)
        print("A new JSON file has been created with the inverted index dictionary")
    
    return None

def json_to_dict(directory):
    with open(directory) as json_file:
            data = json.load(json_file)
            dict_data = dict(data)
    return dict_data