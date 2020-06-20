import pandas as pd

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


if __name__ == '__main__':
    df = get_keyword_df(10000)
    print(df["keyword_name"].tolist())
