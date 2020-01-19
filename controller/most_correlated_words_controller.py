import logging

from flask import jsonify

from controller import app
from logger.logger import setup_logging
from service.keyword_service import request_standard_word

from service.matrix_service import get_most_related_words

setup_logging()
logger = logging.getLogger("fileLogger")


@app.route('/co-occurrence-matrix/most-correlated-words/<string:word>/<int:amount>', methods=['GET'])
def generate_most_correlated_words(word: str, amount: int) -> dict:
    logger.info(f"Received request, word: '{word}'")
    word = request_standard_word(word)
    if word and amount:
        most_correlated_words = get_most_related_words(word, amount + 1)
    else:
        most_correlated_words = None
    result = {"words": most_correlated_words}
    logger.info(f"most correlated words results: {most_correlated_words}")
    return jsonify(result)

