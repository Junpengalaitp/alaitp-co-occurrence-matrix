from collections import OrderedDict

import numpy as np

from co_occurrence_matrix import co_occurrence_matrix


def get_most_related_words(word: str, n: int) -> dict:
    """ word: the query word
        n: top n
    """
    top_n_dict = OrderedDict()
    try:
        word_index = co_occurrence_matrix.keyword_idx_dict[word]
    except KeyError:  # the word does not exist
        return top_n_dict

    # get the row of the word we are looking for
    co_occurred_word_list = co_occurrence_matrix.entity_entity_matrix[word_index]
    co_occurred_word_list_by_category = get_category_words(co_occurred_word_list)
    # Sort the index by value, return indices of the highest value to the lowest
    top_n_indices = np.argsort(co_occurred_word_list_by_category)[::-1][0:n]
    top_n_counts = co_occurred_word_list_by_category[top_n_indices]
    for i, idx in enumerate(top_n_indices):
        keyword = co_occurrence_matrix.unique_keyword[idx]
        if keyword != word:  # remove word itself
            top_n_dict[keyword] = top_n_counts[i]
    return top_n_dict


def get_category_words(co_occurred_word_list: np.ndarray, categories: list = None) -> np.ndarray:
    if not categories:
        return co_occurred_word_list
    else:
        remove_list = []
        for i, j in enumerate(co_occurred_word_list):
            word = co_occurrence_matrix.unique_keyword[i]
            category = co_occurrence_matrix.keyword_category_map[word]
            if category not in categories:
                remove_list.append(i)
                print(word, category, "removed")
        result_list = np.delete(co_occurred_word_list, remove_list)
        return result_list
