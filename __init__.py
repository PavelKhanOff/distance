import logging

from flask import Flask

from .distance.views import distance
from .site.views import site

logging.basicConfig(
    filename='.log', level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def create_app():
    """Создание головного app"""
    app = Flask(__name__)

    app.register_blueprint(distance)
    app.register_blueprint(site)

    return app
