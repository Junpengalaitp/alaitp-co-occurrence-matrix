import pandas as pd

from database.sql_operation.standard_word import select_keywords


def get_keywords_df(limit: int) -> pd.DataFrame:
    df = select_keywords(limit)
    return df


if __name__ == '__main__':
    df = get_keywords_df(10000)
    print(df)