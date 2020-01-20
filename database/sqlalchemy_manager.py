import logging

from sqlalchemy import create_engine

from config.read_config import get_config
from logger.logger import setup_logging

SERVER_IP = get_config('SQL_SERVER', 'IP')
PORT = get_config('SQL_SERVER', 'PORT')
DB_NAME = get_config('SQL_SERVER', 'DB')
username = get_config('SQL_SERVER', 'USER')
password = get_config('SQL_SERVER', 'PASSWORD')

conn = create_engine(
    f'mysql+mysqlconnector://{username}:{password}@{SERVER_IP}:{PORT}/{DB_NAME}?charset=utf8', pool_recycle=3600)

setup_logging()
logger = logging.getLogger("dbLogger")
