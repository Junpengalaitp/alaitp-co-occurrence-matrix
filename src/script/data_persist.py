import os
from concurrent.futures.thread import ThreadPoolExecutor

from loguru import logger

from src.concurrency.CountDownLatch import CountDownLatch
from src.concurrency.PersistIndexThread import PersistIndexThread
from src.database.sql_operation.co_occurrence import truncate
from src.main.co_occurrence_matrix import co_occurrence_matrix
from src.util.timer import timeit


@timeit
def persist_sorted_words():
    table = "co_occurrence_matrix"
    truncate(table)
    threads = [PersistIndexThread(idx, row) for idx, row in enumerate(co_occurrence_matrix.entity_entity_matrix)]
    count_down_latch = CountDownLatch(len(threads))
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 4) as executor:
        for thread in threads:
            executor.submit(thread.run(count_down_latch))
    logger.info("all sorted_word_to_idx persisted")


if __name__ == '__main__':
    persist_sorted_words()


