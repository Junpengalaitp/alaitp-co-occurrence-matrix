import time

from logger.logger import log


def timeit(method):
    def timed(*args, **kw):
        start = time.perf_counter()
        result = method(*args, **kw)
        end = time.perf_counter()
        log.info(f"{method.__name__} finished in {round(end - start, 4)} seconds")
        return result
    return timed
