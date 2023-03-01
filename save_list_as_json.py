import json


# Save the list to a file
def save_list(file, value):
    saved_data = {}
    with open('save/data.json', 'r') as f:
        saved_data = json.load(f)
    saved_data[file] = value
    with open('save/data.json', 'w') as f:
        json.dump(saved_data, f)


# Load the list from the file
def read_list(file):
    saved_data = {}
    with open('save/data.json', 'r') as f:
        saved_data = json.load(f)
    return saved_data[file]


# Load the list from the file
def read_all():
    saved_data = {}
    with open('save/data.json', 'r') as f:
        saved_data = json.load(f)
    return saved_data


def reset():
    with open('save/data.json', 'w') as f:
        clear = {}
        json.dump(clear, f)

