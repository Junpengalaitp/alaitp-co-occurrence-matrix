import pandas as pd
import requests

from database.sql_operation.standard_word import select_keywords


def get_keywords_df(limit: int) -> pd.DataFrame:
    df = select_keywords(limit)
    standardize_keyword(df)
    return df


def standardize_keyword(keyword_df: pd.DataFrame):
    distinct_words = keyword_df.keyword_name.unique()
    for word in distinct_words:
        standard_word = request_standard_word(word)
        keyword_df.loc[keyword_df.keyword_name == word, "keyword_name"] = standard_word


def request_standard_word(word: str) -> str:
    r = requests.get(f"http://127.0.0.1:8812/standardize-word/{word}")
    if r and r.status_code == 200:
        return r.text


if __name__ == '__main__':
    df = get_keywords_df(10000)
    standardize_keyword(df)
    print(df["keyword_name"].tolist())
