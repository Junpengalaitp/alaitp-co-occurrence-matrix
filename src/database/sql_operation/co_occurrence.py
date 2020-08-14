import numpy as np

from src.config.sql_config import conn
from src.main.co_occurrence_matrix import co_occurrence_matrix


def insert_idx_to_word(idx: int, word: str) -> None:
    query = f"""
                INSERT INTO co_occurrence_idx_to_word
                VALUES ({idx}, '{word}')
             """
    conn.execute(query)


def insert_sorted_word_to_idx(word: str, word_counts: str, sorted_indices: str) -> None:
    query = f"""
                INSERT INTO co_occurrence_word_count (word, word_counts, sorted_indices)
                VALUES ('{word}', '{word_counts}', '{sorted_indices}')
             """
    conn.execute(query)


if __name__ == '__main__':
    for idx, word in enumerate(co_occurrence_matrix.unique_keyword):
        insert_idx_to_word(idx, word)

    for row_idx, row in enumerate(co_occurrence_matrix.entity_entity_matrix):
        word_count = ",".join([str(n) for n in row])
        sorted_indices = ",".join([str(n) for n in np.argsort(row)[::-1]])
        insert_sorted_word_to_idx(co_occurrence_matrix.unique_keyword[row_idx], word_count, sorted_indices)
