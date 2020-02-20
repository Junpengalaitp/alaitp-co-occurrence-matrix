import pandas as pd

from database.sqlalchemy_manager import conn


def select_keywords(limit):
    query = f"""
                SELECT job_id, job_title, standard_word, keyword_type, count 
                FROM keywords_job_model
                WHERE standard_word IS NOT NULL 
                LIMIT {limit}
             """
    return pd.read_sql_query(query, conn)


