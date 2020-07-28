"""redis cache operations"""

import json
from typing import Optional

import numpy as np
import pandas as pd
from loguru import logger

from config.redis_config import redis_template
from constant.constant import KEYWORD_DF_KEY, MATRIX_KEY

enable_cache = True


def store_keyword_df_cache(df: pd.DataFrame):
    if not enable_cache:
        return
    redis_template.db(0).set(KEYWORD_DF_KEY, df.to_msgpack(compress="zlib"))
    logger.info("stored the keyword_df in redis as cache")


def get_keyword_df_cache() -> Optional[pd.DataFrame]:
    if not enable_cache:
        return
    cache = redis_template.db(0).get(KEYWORD_DF_KEY)
    if cache:
        logger.info("found the keyword_df cache in redis")
        return pd.read_msgpack(cache)


def store_matrix_cache(matrix: np.ndarray):
    if not enable_cache:
        return
    redis_template.db(0).set(MATRIX_KEY, json.dumps(matrix.tolist()))
    logger.info("stored the matrix in redis as cache")


def get_matrix_cache() -> Optional[np.ndarray]:
    if not enable_cache:
        return
    cache = redis_template.db(0).get(MATRIX_KEY)
    if cache:
        logger.info("found matrix cache in redis")
        return np.asarray(json.loads(cache), dtype=np.int16)


def standard_word_cache_exist(other_word: str):
    cache = redis_template.db(3).get(other_word)
    if cache:
        return True
    return False


def get_standard_word_cache(other_word: str) -> str:
    cache = redis_template.db(3).get(other_word)
    if cache:
        return cache.decode("utf-8")
    else:
        return other_word


def set_standard_word_cache(other_word: str, standard_word: str):
    if not enable_cache:
        return
    redis_template.db(3).set(other_word, standard_word)
    logger.info(f"stored the standard word: {standard_word} of {other_word} in redis as cache")
