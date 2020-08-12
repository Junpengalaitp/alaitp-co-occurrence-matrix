from py_eureka_client import eureka_client

from src.config.config_server import CONFIG


def connect_eureka(ip, port):
    eureka_client.init(eureka_server=CONFIG['eureka.client.serviceUrl.defaultZone'],
                       app_name="matrix",
                       instance_host=ip,
                       instance_port=port,
                       ha_strategy=eureka_client.HA_STRATEGY_OTHER)
