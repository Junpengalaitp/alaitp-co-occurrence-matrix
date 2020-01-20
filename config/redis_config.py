import redis

from config.read_config import get_config

SERVER_IP = get_config('REDIS', 'IP')
PORT = get_config('REDIS', 'PORT')
DB = get_config('REDIS', 'DB')

pool = redis.ConnectionPool(host=SERVER_IP, port=PORT, db=DB)

redis_template = redis.Redis(connection_pool=pool)
