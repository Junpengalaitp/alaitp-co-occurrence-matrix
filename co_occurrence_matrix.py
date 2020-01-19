import logging
import os
from collections import defaultdict

import numpy as np

from logger.logger import setup_logging
from service.keyword_service import get_keywords_df

setup_logging()
logger = logging.getLogger("fileLogger")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoOccurrenceMatrix:
    """ DataManager used to load the data from Database and keep it in memory, this is a Singleton class """

    # Apply singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.keyword_df = get_keywords_df(10000)
        self.unique_keyword = list(self.keyword_df.keyword_name.unique())
        self.keyword_idx = [self.unique_keyword.index(word) for word in self.unique_keyword]
        self.keyword_dict = dict(zip(self.unique_keyword, self.keyword_idx))
        self.idx_to_keyword = dict(zip(self.keyword_idx, self.unique_keyword))

        self.entity_entity_matrix = self._get_entity_entity_matrix()
        logger.info(f"loaded entity_entity_matrix, size(row * column): {self.entity_entity_matrix.shape}")

    def _get_entity_entity_matrix(self):
        entity_entity_matrix = np.zeros((len(self.unique_keyword), len(self.unique_keyword)), np.float64)
        keyword_dict = defaultdict(list)
        for row in self.keyword_df.itertuples():
            # Check whether the job_id exist
            keyword_tuple = (row.keyword_name, row.count, row.keyword_type)
            job_id = row.job_id
            keyword_dict[job_id].append(keyword_tuple)

        for key in keyword_dict:
            for item in keyword_dict[key]:
                row_idx = self.keyword_dict[item[0]]
                for word in keyword_dict[key]:
                    col_idx = self.keyword_dict[word[0]]
                    entity_entity_matrix[row_idx, col_idx] += 1
        return entity_entity_matrix

    def reload_co_occurrence_matrix(self):
        self.__init__()


# init singleton
co_occurrence_matrix = CoOccurrenceMatrix()



