import requests


def config_from_config_server():
    r = requests.get("http://localhost:8810/co-occurrence-matrix/default")
    res = r.json()
    config = {}
    for cfg in res['propertySources']:
        config.update(cfg['source'])
    return config


CONFIG = config_from_config_server()

if __name__ == '__main__':
    print(config_from_config_server())
