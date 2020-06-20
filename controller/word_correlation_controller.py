from flask import jsonify
from loguru import logger

from constants.category import category_dict
from controller import app
from service.cache_service import get_standard_word_cache
from service.matrix_service import get_most_related_words

no_word_found_res = {"oops, no correlated word found": {"count": 1, "category": "AI"}}  # dummy data for no res


@app.route('/most-correlated-words/<string:word>/<int:amount>/<string:categories>', methods=['GET'])
def generate_most_correlated_words(word: str, amount: int, categories: str = None) -> dict:
    logger.info(f"Received request, word: '{word}'")
    word = get_standard_word_cache(word)
    if word and amount:
        if "all" in categories:
            category_list = None
        else:
            category_list = [category_dict[ct] for ct in categories.split(",")]
        most_correlated_words = get_most_related_words(word, amount, category_list)
    else:
        most_correlated_words = no_word_found_res
    if not most_correlated_words:
        most_correlated_words = no_word_found_res
    result = {"words": most_correlated_words}
    logger.info(f"most correlated words results: {most_correlated_words}")
    return jsonify(result)

