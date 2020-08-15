"""Manual implementation of spring cloud config, request config on app start and store them in cache"""

import requests

env = "test"
config_server_url = "192.168.31.21:8810"


def config_from_config_server():
    r = requests.get(f"http://{config_server_url}/co-occurrence-matrix/{env}")
    res = r.json()
    config = {}
    for cfg in res['propertySources']:
        config.update(cfg['source'])
    return config


CONFIG = config_from_config_server()

if __name__ == '__main__':
    print(config_from_config_server())
