from loguru import logger

from src.config.sql_config import conn


def truncate(table_name: str):
    query = f"TRUNCATE {table_name}"
    conn.execute(query)
    logger.info(f"{table_name} truncated")

