import logging
from os.path import abspath

from flask import Flask, g, request, Response

from .blueprints.api import api
from .logic import button


def create_app() -> Flask:
    logging.info("aaaaa")
    button.setup()
    app = Flask(
        __name__,
        static_folder=abspath('public'),
        static_url_path='/'
    )

    app.register_blueprint(api)

    return app
