from loguru import logger

from src.config.sql_config import conn


def truncate(table_name: str):
    query = f"TRUNCATE {table_name}"
    conn.execute(query)
    logger.info(f"{table_name} truncated")


def insert_idx_to_word(idx: int, word: str, category: str) -> None:
    query = f"""
                INSERT INTO co_occurrence_idx_to_word (idx, word, category)
                VALUES ({idx}, '{word}', '{category}')
             """
    conn.execute(query)


def insert_sorted_word_to_idx(word: str, word_counts: str, sorted_indices: str) -> None:
    query = f"""
                INSERT INTO co_occurrence_word_count (word, word_counts, sorted_indices)
                VALUES ('{word}', '{word_counts}', '{sorted_indices}')
             """
    conn.execute(query)
