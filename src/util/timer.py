import time

from loguru import logger


def timeit(method):
    def timed(*args, **kw):
        start = time.perf_counter()
        result = method(*args, **kw)
        end = time.perf_counter()
        logger.info(f"{method.__name__} finished in {round(end - start, 4)} seconds")
        return result
    return timed
