from flask import Flask

app = Flask(__name__)

from .most_correlated_words_controller import generate_most_correlated_words

