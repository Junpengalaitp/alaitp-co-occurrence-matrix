from collections import OrderedDict
import pprint

import numpy as np

from co_occurrence_matrix import co_occurrence_matrix

pp = pprint.PrettyPrinter()


def get_most_related_words(word: str, n: int, categories: list = None) -> dict:
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
    # Sort the index by value, return indices of the highest value to the lowest
    sorted_indices = np.argsort(co_occurred_word_list)[::-1]
    top_n_indices = get_top_n_by_categories(sorted_indices, n, categories)
    top_n_counts = co_occurred_word_list[top_n_indices]
    for i, idx in enumerate(top_n_indices):
        try:
            keyword = co_occurrence_matrix.unique_keyword[idx]
        except IndexError:
            continue
        if keyword != word and top_n_counts[i] != 0:  # remove word itself and count 0 words
            top_n_dict[keyword] = top_n_counts[i]
    return top_n_dict


def get_top_n_by_categories(sorted_indices: np.ndarray, count: int = 10, categories: list = None) -> np.ndarray:
    if not categories:
        return sorted_indices[0:count+1]
    else:
        index_in_category = []
        for index in sorted_indices:
            try:
                word = co_occurrence_matrix.unique_keyword[index]
            except IndexError:
                continue
            category = co_occurrence_matrix.keyword_category_map[word]
            if category in categories:
                index_in_category.append(index)
                if len(index_in_category) > count:
                    break
        return np.asarray(index_in_category, dtype=np.int32)


