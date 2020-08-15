from collections import defaultdict
from threading import Thread

import numpy as np
import pandas as pd
from loguru import logger

from src.concurrency.CountDownLatch import CountDownLatch
from src.config.sql_config import conn
from src.main.co_occurrence_matrix import co_occurrence_matrix


class PersistIndexThread(Thread):
    def __init__(self, row_idx, df_row):
        super().__init__()
        self.row_idx = row_idx
        self.df_row = df_row

    def run(self, count_down: CountDownLatch) -> None:
        super().run()
        count_down.count_down()
        word_count = ",".join([str(n) for n in self.df_row])
        sorted_indices = ",".join([str(n) for n in reversed(np.argsort(self.df_row))])
        sorted_word_to_idx_dict = defaultdict(list)
        word = co_occurrence_matrix.unique_keyword[self.row_idx]
        sorted_word_to_idx_dict["word"].append(word)
        sorted_word_to_idx_dict["sorted_indices"].append(sorted_indices)
        sorted_word_to_idx_dict["word_counts"].append(word_count)

        sorted_word_to_idx_df = pd.DataFrame(data=sorted_word_to_idx_dict)
        table = "co_occurrence_word_count"
        sorted_word_to_idx_df.to_sql(name=table, con=conn, if_exists="append", index=False)

        logger.info(f"sorted_word_to_idx for word: {word} persisted, remaining works: {count_down.count}")
