from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler

app = Flask(__name__)
cors = CORS(app, resources={r"/hotspot-generator/*": {"origins": "*"}})
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

app.config['CORS_HEADERS'] = 'Content-Type'

from .most_correlated_words_controller import generate_most_correlated_words

