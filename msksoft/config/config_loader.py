import yaml

# Load the YAML configuration file
with open('D:\projects\multispectral_harvest_defect_detection_3d_projection\config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def get(path):
    return config[path]
