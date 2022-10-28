from os.path import abspath

from flask import Flask

from .blueprints.api import api
from .logic import button


def create_app():
    button.setup()
    app = Flask(
        __name__,
        static_folder=abspath('public'),
        static_url_path='/'
    )

    app.register_blueprint(api)
    return app
