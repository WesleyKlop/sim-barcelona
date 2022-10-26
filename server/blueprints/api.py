from http import HTTPStatus

from flask import Blueprint, request

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!', HTTPStatus.OK
    