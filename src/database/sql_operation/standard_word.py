import pandas as pd

from src.config.sql_config import conn


def select_keywords(limit: int) -> pd.DataFrame:
    query = f"""
                SELECT job_id, standard_word, keyword_type, count
                FROM keywords_job_model
                WHERE standard_word IS NOT NULL
                AND standard_word SIMILAR TO '[a-zA-Z0-9# -+.$]*'
                AND keyword_type NOT IN ('GPE', 'DATE', 'CARDINAL', 'PERSON', 'PERCENT', 'WORK_OF_ART')
                GROUP BY job_id, standard_word, keyword_type, count
                LIMIT {limit}
             """
    return pd.read_sql_query(query, conn)


def select_standard_word(other_word: str) -> str:
    query = f"""
                SELECT standard_word
                FROM standard_word 
                WHERE standard_word = '{other_word}'
             """
    res = conn.execute(query)
    if res.rowcount != 0:
        return res.fetchone()[0]
    else:
        return select_standard_word_by_other_word(other_word)


def select_standard_word_by_other_word(other_word: str) -> str:
    query = f"""
                SELECT standard_word
                FROM standard_word 
                WHERE other_words LIKE '%%,{other_word},%%'
             """
    res = conn.execute(query)
    if res.rowcount != 0:
        return res.fetchone()[0]
    else:
        return other_word


if __name__ == '__main__':
    df = select_keywords(1000)
    print(df)


