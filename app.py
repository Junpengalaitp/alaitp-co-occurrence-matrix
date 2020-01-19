from waitress import serve

from config.read_config import get_config
from controller import app


def start_web_service():
    """Start the service using the IP and PORT configured in the config.ini"""
    host = get_config("WEB_SERVER", "IP")
    port = get_config("WEB_SERVER", "PORT")
    serve(app, host=host, port=port)


if __name__ == '__main__':
    start_web_service()
