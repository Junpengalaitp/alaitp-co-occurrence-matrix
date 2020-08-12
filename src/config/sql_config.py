from sqlalchemy import create_engine

from src.config.config_server import CONFIG

SERVER_URL = CONFIG['spring.datasource.url'].split('//')[1]
username = CONFIG['spring.datasource.username']
password = CONFIG['spring.datasource.password']

conn = create_engine(f'postgresql://{username}:{password}@{SERVER_URL}', pool_recycle=3600)


