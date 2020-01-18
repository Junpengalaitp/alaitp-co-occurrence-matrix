import logging

from flask import jsonify
from flask_cors import cross_origin

from controller import app
from logger.Log import setup_logging
from service.co_coccurrence_service import get_most_related_words
from service.hotspot_tag_service import standardize_word

setup_logging()
logger = logging.getLogger("fileLogger")


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Credentials'] = 'true'
    header['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH, DELETE'

    return response


@app.route('/hotspot-generator/most-correlated-words/<string:word>/<int:amount>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def generate_most_correlated_words(word: str, amount: int) -> dict:
    logger.info(f"Received request, word: '{word}'")
    try:
        word = standardize_word(word)
        if word and amount:
            most_correlated_words = get_most_related_words(word, amount + 1)
        else:
            most_correlated_words = None
        result = {"success": True, "words": most_correlated_words}
        logger.info(f"most correlated words results: {most_correlated_words}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"error: {e}")
        result = {"success": False, "words": {}}
        return jsonify(result)

