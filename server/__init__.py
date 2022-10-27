from os.path import abspath
from threading import Lock

from flask import Flask

from .blueprints.api import api
from .logic import button


button.setup()

app = Flask(
    __name__,
    static_folder=abspath('public'),
    static_url_path='/'
)

app.register_blueprint(api)

app.run(host='0.0.0.0', debug=False)