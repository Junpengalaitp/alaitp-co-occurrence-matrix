import os
from collections import defaultdict

import numpy as np
from loguru import logger

from service.keyword_service import get_keyword_df
from util.timer import timeit

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoOccurrenceMatrix:
    """DataManager used to load the data from Database and keep it in memory, this is a Singleton class"""

    # Apply singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        amount = 300000
        self.keyword_df = get_keyword_df(amount)
        self.unique_keyword = self._get_unique_keyword()
        self.keyword_category_map = self._get_category_map()
        self.keyword_idx_dict = self._get_keyword_idx_dict()
        self.entity_entity_matrix = self._get_entity_entity_matrix()
        logger.info(f"loaded entity_entity_matrix, size(row * column): {self.entity_entity_matrix.shape}")

    @timeit
    def _get_unique_keyword(self) -> list:
        """:return: list of unique keywords"""
        return list(self.keyword_df.standard_word.unique())

    @timeit
    def _get_keyword_idx_dict(self) -> dict:
        """:return: dict of key and value: (keyword: keyword index)"""
        return {word: idx for idx, word in enumerate(self.unique_keyword)}

    @timeit
    def _get_category_map(self) -> dict:
        """:return: dict of key and value: (keyword: keyword category)"""
        category_map = defaultdict(str)
        for row in self.keyword_df.itertuples():
            category_map[row.standard_word] = row.keyword_type
        return category_map

    @timeit
    def _get_entity_entity_matrix(self) -> np.ndarray:
        """build the co-occurrence matrix, group the keyword by the job, if two keywords both occurred in a job,
           increment their co-occurrence value by one
           :return: entity_entity_matrix with the keyword indices as row and col, co-occurrence value of the two
                    keywords as value.
        """
        entity_entity_matrix = np.zeros((len(self.unique_keyword), len(self.unique_keyword)), np.float64)
        keyword_dict = defaultdict(list)
        for row in self.keyword_df.itertuples():
            # Check whether the job_id exist
            keyword_tuple = (row.standard_word, row.count, row.keyword_type)
            job_id = row.job_id
            keyword_dict[job_id].append(keyword_tuple)

        for job_id in keyword_dict:
            for item in keyword_dict[job_id]:
                row_idx = self.keyword_idx_dict[item[0]]
                for word in keyword_dict[job_id]:
                    col_idx = self.keyword_idx_dict[word[0]]
                    entity_entity_matrix[row_idx, col_idx] += 1
        return entity_entity_matrix

    def reload_co_occurrence_matrix(self):
        self.__init__()


# init singleton
co_occurrence_matrix = CoOccurrenceMatrix()
