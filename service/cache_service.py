import json
from typing import Optional

import numpy as np
import pandas as pd

from config.read_config import get_config
from config.redis_config import redis_template
from constants.constants import KEYWORD_DF_KEY, MATRIX_KEY
from logger.logger import log

enable_cache = bool(int(get_config('CACHE', 'ON')))


def store_keyword_df_cache(df: pd.DataFrame):
    redis_template.set(KEYWORD_DF_KEY, df.to_msgpack(compress="zlib"))
    log.info("stored the keyword_df in redis as cache")


def get_keyword_df_cache() -> Optional[pd.DataFrame]:
    if not enable_cache:
        return
    cache = redis_template.get(KEYWORD_DF_KEY)
    if cache:
        log.info("found the keyword_df cache in redis")
        return pd.read_msgpack(cache)


def store_matrix_cache(matrix: np.ndarray):
    redis_template.set(MATRIX_KEY, json.dumps(matrix.tolist()))
    log.info("stored the matrix in redis as cache")


def get_matrix_cache() -> Optional[np.ndarray]:
    if not enable_cache:
        return
    cache = redis_template.get(MATRIX_KEY)
    if cache:
        log.info("found matrix cache in redis")
        return np.asarray(json.loads(cache), dtype=np.float64)