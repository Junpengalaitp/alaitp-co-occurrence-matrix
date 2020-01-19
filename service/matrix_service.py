from collections import OrderedDict

import numpy as np

from co_occurrence_matrix import co_occurrence_matrix


def get_most_related_words(word: str, n: int) -> dict:
    """ word: the query word
        n: top n
    """
    top_n_dict = OrderedDict()
    try:
        word_index = co_occurrence_matrix.keyword_dict[word]
    except KeyError:  # the word does not exist
        return top_n_dict
    # Sort the index by value, return indices of the highest value to the lowest
    top_n_indices = np.argsort(co_occurrence_matrix.entity_entity_matrix[word_index])[::-1][0:n]
    top_n_counts = co_occurrence_matrix.entity_entity_matrix[word_index][top_n_indices]
    for i, idx in enumerate(top_n_indices):
        keyword = co_occurrence_matrix.idx_to_keyword[idx]
        if keyword != word:  # remove word itself
            top_n_dict[keyword] = top_n_counts[i]
    return top_n_dict
