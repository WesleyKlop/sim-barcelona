import os.path
from http import HTTPStatus
from os.path import abspath

import flask
from flask import Blueprint, Response, render_template

from server.logic.announcer import announcer, format_sse
from server.logic.camera import take_picture
from server.logic.image import ImageGenerator

api = Blueprint('api', __name__, url_prefix='/api')

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
    announcer.log('Got request on test')
    generator = ImageGenerator()
    announcer.log('Created image generator')

    img_path = take_picture(abspath('public/results'))
    announcer.announce(
        format_sse(flask.url_for('static', filename='results/' + os.path.basename(img_path)), 'start'))
    if img_path is None:
        announcer.log('Failed to take picture')
        return 'Failure', HTTPStatus.IM_A_TEAPOT
    announcer.log('Got picture')

    result = generator.generate(img_path, abspath('public/results'))
    announcer.announce(
        format_sse(flask.url_for('static', filename='results/' + result), 'result')
    )
    return result + '\n', HTTPStatus.OK
