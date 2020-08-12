from flask import Flask

app = Flask(__name__)

from .word_correlation_controller import generate_most_correlated_words

