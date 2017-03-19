import logging.config
import os

from flask import Flask

from .config import LOGGING

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))

app.url_map.strict_slashes = False

logging.config.dictConfig(LOGGING)

from app import route

