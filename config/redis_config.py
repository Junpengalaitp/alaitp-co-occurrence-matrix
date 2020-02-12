import redis

from config.config_server import CONFIG

HOST = CONFIG['spring.redis.host']
PORT = CONFIG['spring.redis.port']
DB = CONFIG['spring.redis.database']

pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB)

redis_template = redis.Redis(connection_pool=pool)
