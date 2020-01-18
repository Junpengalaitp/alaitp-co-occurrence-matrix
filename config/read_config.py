import os
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, 'config', 'dev_config.ini')


def get_config(section, key):
    config = ConfigParser()
    config.read(config_path)
    return config.get(section, key)
