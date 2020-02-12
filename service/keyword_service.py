import pandas as pd
import requests

from database.sql_operation.standard_word import select_keywords
from service.cache_service import get_keyword_df_cache
from util.timer import timeit


@timeit
def get_keyword_df(limit: int) -> pd.DataFrame:
    cache = get_keyword_df_cache()
    if isinstance(cache, pd.DataFrame):
        return cache
    else:
        df = select_keywords(limit)
    return df


def request_standard_word(word: str) -> str:
    r = requests.get(f"http://localhost:8888/word-standardization/standardize-word/{word}")
    if r and r.status_code == 200:
        return r.text


if __name__ == '__main__':
    df = get_keyword_df(10000)
    print(df["keyword_name"].tolist())
