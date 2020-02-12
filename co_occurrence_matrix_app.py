from random import randint

from waitress import serve

from config.config_server import CONFIG
from config.eureka_config import connect_eureka
from controller import app


def start_web_service():
    """Start the service using the IP and PORT configured in the config.ini"""
    SERVER_IP = CONFIG['web.server.ip']
    PORT = randint(27018, 65535)
    connect_eureka(SERVER_IP, PORT)
    serve(app, host=SERVER_IP, port=PORT)


if __name__ == '__main__':
    start_web_service()
