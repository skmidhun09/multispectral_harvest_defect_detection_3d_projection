import json
from msksoft.config import config_loader as cfg

path = str(cfg.get('datastore'))


# Save the list to a file
def save_list(file, value):
    with open(path, 'r') as f:
        saved_data = json.load(f)
    saved_data[file] = value
    with open(path, 'w') as f:
        json.dump(saved_data, f)


# Load the list from the file
def read_list(file):
    with open(path, 'r') as f:
        saved_data = json.load(f)
    return saved_data[file]


# Load the list from the file
def read_all():
    with open(path, 'r') as f:
        saved_data = json.load(f)
    return saved_data


# Reset the file content
def reset():
    with open(path, 'w') as f:
        clear = {}
        json.dump(clear, f)
