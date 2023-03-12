import yaml

# Load the YAML configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def get(path):
    return config[path]
