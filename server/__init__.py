from flask import Flask
from os.path import abspath

from .blueprints.api import api


def create_app() -> Flask:
    print()
    app = Flask(
        __name__,
        static_folder=abspath('public'),
        static_url_path='/'
    )

    app.register_blueprint(api)

    return app
