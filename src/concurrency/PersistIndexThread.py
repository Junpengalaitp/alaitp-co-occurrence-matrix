from threading import Thread

import numpy as np
import pandas as pd
from loguru import logger

from src.concurrency.CountDownLatch import CountDownLatch
from src.config.sql_config import conn
from src.constant.category import category_map
from src.main.co_occurrence_matrix import co_occurrence_matrix


class PersistIndexThread(Thread):
    def __init__(self, row_idx, df_row):
        super().__init__()
        self.row_idx = row_idx
        self.df_row = df_row

    def run(self, count_down_latch: CountDownLatch) -> None:
        super().run()
        count_down_latch.count_down()
        # for each category, persist top 100 words only to save disk space
        sorted_indices = np.argsort(self.df_row)[::-1][:len(category_map) * 100]
        sorted_co_occurred_word_info_text = ""
        for idx in sorted_indices:
            co_occurred_word = co_occurrence_matrix.unique_keyword[idx]
            category = co_occurrence_matrix.keyword_category_map[co_occurred_word]
            category_abbr = category_map.get(category, category)  # use abbr to save disk space
            count = str(self.df_row[idx])
            co_occurred_word_info_str_repr = f"{co_occurred_word}|{category_abbr}|{count}"
            sorted_co_occurred_word_info_text += co_occurred_word_info_str_repr + ","

        sorted_word_to_idx_dict = {}
        word = co_occurrence_matrix.unique_keyword[self.row_idx]
        sorted_word_to_idx_dict["word"] = [word]
        sorted_word_to_idx_dict["co_occurred_word_info_sorted"] = [sorted_co_occurred_word_info_text[:-1]]  # remove trailing comma

        sorted_word_to_idx_df = pd.DataFrame(data=sorted_word_to_idx_dict)
        table = "co_occurrence_matrix"
        sorted_word_to_idx_df.to_sql(name=table, con=conn, if_exists="append", index=False)

        logger.info(f" remaining works: {count_down_latch.count}, matrix row for word: {word} persisted")
