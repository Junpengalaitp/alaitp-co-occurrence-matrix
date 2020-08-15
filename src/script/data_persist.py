import os
import traceback
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor

import pandas as pd
from loguru import logger

from src.concurrency.CountDownLatch import CountDownLatch
from src.concurrency.PersistIndexThread import PersistIndexThread
from src.config.sql_config import conn
from src.database.sql_operation.co_occurrence import truncate
from src.main.co_occurrence_matrix import co_occurrence_matrix


def persist_word_to_index():
    idx_to_word_dict = defaultdict(list)
    for idx, word in enumerate(co_occurrence_matrix.unique_keyword):
        try:
            idx_to_word_dict["idx"].append(idx)
            idx_to_word_dict["word"].append(word)
            idx_to_word_dict["category"].append(co_occurrence_matrix.keyword_category_map.get(word))
        except:
            traceback.print_exc()
            logger.error(f"error word: {word}")
            continue

    idx_to_word_df = pd.DataFrame(data=idx_to_word_dict)
    table = "co_occurrence_idx_to_word"
    truncate(table)
    idx_to_word_df.to_sql(name=table, con=conn, if_exists="append", index=False)
    logger.info("idx_to_word persisted")


def persist_sorted_indices():
    table = "co_occurrence_word_count"
    truncate(table)

    threads = [PersistIndexThread(idx, row) for idx, row in enumerate(co_occurrence_matrix.entity_entity_matrix)]
    count_down_latch = CountDownLatch(len(threads))
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 4) as executor:
        for thread in threads:
            executor.submit(thread.run(count_down_latch))

    logger.info("all sorted_word_to_idx persisted")


if __name__ == '__main__':
    persist_word_to_index()
    persist_sorted_indices()


