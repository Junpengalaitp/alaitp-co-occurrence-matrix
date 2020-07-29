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
        amount = 1000000
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
        # use np.int16 here to minimize memory usage
        entity_entity_matrix = np.zeros((len(self.unique_keyword), len(self.unique_keyword)), np.int16)
        # aggregate keywords by job
        keyword_dict = self._get_job_keyword_collection_dict()

        # build the matrix, pair each word with all other words for every job keyword collection
        for job_keywords in keyword_dict.values():
            for row_word in job_keywords:
                row_idx = self.keyword_idx_dict[row_word]
                for col_word in job_keywords:
                    col_idx = self.keyword_idx_dict[col_word]
                    entity_entity_matrix[row_idx, col_idx] += 1
        return entity_entity_matrix

    def _get_job_keyword_collection_dict(self) -> dict:
        """:return: dict of key and value: (job_id, keyword collection)"""
        job_keyword_list_dict = defaultdict(list)
        for row in self.keyword_df.itertuples():
            job_keyword_list_dict[row.job_id].append(row.standard_word)
        return job_keyword_list_dict

    def reload_co_occurrence_matrix(self):
        self.__init__()


# init singleton
co_occurrence_matrix = CoOccurrenceMatrix()
