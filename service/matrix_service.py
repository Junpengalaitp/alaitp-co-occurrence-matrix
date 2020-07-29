import heapq

import numpy as np
from loguru import logger

from main.co_occurrence_matrix import co_occurrence_matrix
from util.timer import timeit


def get_most_related_words(word: str, n: int, categories: list = None) -> dict:
    """
    get top n for correlated words for word by the categories
    :param word: the root word for correlated words
    :param n: top n
    :param categories: correlated words category
    :returns: dict of top n keyword (key: keyword, value: json of count and category))
    """
    top_n_dict = {}
    try:
        word_index = co_occurrence_matrix.keyword_idx_dict[word]
    except KeyError:  # the word does not exist
        logger.warning(f"the word: '{word}' does not exist in cache")
        return top_n_dict

    # get the row of the word we are looking for
    co_occurred_word_list = co_occurrence_matrix.entity_entity_matrix[word_index]

    top_n_indices = get_top_n_by_category(co_occurred_word_list, n, categories)
    for idx in top_n_indices:
        try:
            keyword = co_occurrence_matrix.unique_keyword[idx]
        except IndexError:
            continue
        if keyword != word and co_occurred_word_list[idx] != 0:  # skip word itself and count 0 words
            count = int(co_occurred_word_list[idx])  # convert to normal int, np.int is not json serializable
            top_n_dict[keyword] = {
                "count": count,
                "category": co_occurrence_matrix.keyword_category_map[keyword]
            }
    return top_n_dict


@DeprecationWarning
@timeit
def get_top_n_by_categories(co_occurred_word_list: np.ndarray, count: int, categories: list = None) -> list:
    """
    select top n in the sorted_indices by the categories(sorting implementation)
    :param co_occurred_word_list: the row of co-occurred words of the target word
    :param count: top n
    :param categories: co-occurred words category, if None, accept all categories
    :returns: indices of top n word
    """
    # Sort the index by value, return indices of the highest value to the lowest
    sorted_indices = np.argsort(co_occurred_word_list)[::-1]
    if not categories:
        return sorted_indices[0:count + 1]
    else:
        index_in_category = []
        for index in sorted_indices:
            try:
                keyword = co_occurrence_matrix.unique_keyword[index]
            except IndexError:
                continue
            category = co_occurrence_matrix.keyword_category_map[keyword]
            if category in categories:
                index_in_category.append(index)
                if len(index_in_category) > count:
                    break
        return index_in_category


@timeit
def get_top_n_by_category(co_occurred_word_list: np.ndarray, count: int, categories: list = None) -> list:
    """
    select top n in the sorted_indices by the categories(heap implementation)
    :param co_occurred_word_list: the row of co-occurred words of the target word
    :param count: top n
    :param categories: co-occurred words category, if None, accept all categories
    :returns: indices of top n word
    """
    co_occurred_word_heap = [(-v, idx) for idx, v in enumerate(co_occurred_word_list)]  # negative value for max heap
    heapq.heapify(co_occurred_word_heap)
    index_in_category = []

    while len(index_in_category) < count and len(co_occurred_word_heap) != 0:
        top_word_count, top_word_idx = heapq.heappop(co_occurred_word_heap)
        try:
            keyword = co_occurrence_matrix.unique_keyword[top_word_idx]
        except IndexError:
            continue

        category = co_occurrence_matrix.keyword_category_map[keyword]
        if not categories or category in categories:
            index_in_category.append(top_word_idx)

    return index_in_category
