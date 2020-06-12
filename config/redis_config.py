import redis
from redis import Redis

from config.config_server import CONFIG

HOST = CONFIG['spring.redis.host']
PORT = CONFIG['spring.redis.port']
DB0 = CONFIG['spring.redis.job.co.occurrence']
DB1 = CONFIG['spring.redis.job.api']
DB2 = CONFIG['spring.redis.database']
DB3 = CONFIG['spring.redis.standard.word']
DB4 = CONFIG['spring.redis.standard.category']


class RedisTemplate:
    # Apply singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.co_occurrence = redis.ConnectionPool(host=HOST, port=PORT, db=DB0)
        self.job_search_pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB1)
        self.job_keyword_pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB2)
        self.standard_word_pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB3)
        self.standard_category_pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB4)

    def db(self, db: int) -> Redis:
        if db == 0:
            return Redis(connection_pool=self.co_occurrence)
        if db == 1:
            return Redis(connection_pool=self.job_search_pool)
        if db == 2:
            return Redis(connection_pool=self.job_keyword_pool)
        if db == 3:
            return Redis(connection_pool=self.standard_word_pool)
        if db == 4:
            return Redis(connection_pool=self.standard_category_pool)


redis_template = RedisTemplate()
