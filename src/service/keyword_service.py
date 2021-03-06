from src.database.sql_operation.standard_word import select_keywords, select_standard_word
from src.service.cache_service import *
from src.util.timer import timeit


@timeit
def get_keyword_df(limit: int) -> pd.DataFrame:
    """get the keyword df from cache if exist, else get it from SQL DB"""
    return select_keywords(limit)


def get_standard_word(other_word: str) -> str:
    """get the standard word from cache if exist, else get it from SQL DB"""
    if standard_word_cache_exist(other_word):
        standard_word = get_standard_word_cache(other_word)
    else:
        standard_word = select_standard_word(other_word)
        set_standard_word_cache(other_word, standard_word)
    logger.info(f"get the standard word: {standard_word} of {other_word}")
    return standard_word
