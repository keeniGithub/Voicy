import json
import config

def select_radio(name):
    with open(config.RadioListJson_path, 'r') as f:
        data = json.load(f)
        return data.get(name)

def radio_list():
    with open(config.RadioListJson_path) as f:
        data = json.load(f)
        all_keys = list(data.keys())
        return all_keys