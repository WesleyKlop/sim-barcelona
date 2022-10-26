from http import HTTPStatus

from flask import Blueprint, Response
from server.logic.announcer import announcer
from server.logic import format_sse
from server.logic.image import ImageGenerator
from server.logic.camera import take_picture

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/hello', methods=['GET'])
def hello():
    announcer.announce(format_sse('Hello, world!'))
    return 'Hello World!', HTTPStatus.OK
    
@api.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')

@api.route('/test', methods=['GET'])
def test():
    generator = ImageGenerator()

    img_path = take_picture()
    result = generator.generate('/Users/wesley/Downloads/litter.jpeg')
    return result, HTTPStatus.OK

