from random import randint

from waitress import serve

from src.config.config_server import CONFIG
from src.config.eureka_config import connect_eureka
from src.controller import app


def start_web_service():
    """Start the waitress server using the IP and PORT configured in the config.ini"""
    SERVER_IP = CONFIG['web.server.ip']
    PORT = randint(27018, 65535)
    connect_eureka(SERVER_IP, PORT)
    serve(app, host="0.0.0.0", port=PORT)


def start_test_server():
    """Start the dev server"""
    SERVER_IP = CONFIG['web.server.ip']
    PORT = 5001
    connect_eureka(SERVER_IP, PORT)
    app.run(host="0.0.0.0", port=PORT)


if __name__ == '__main__':
    # start_web_service()
    start_test_server()
