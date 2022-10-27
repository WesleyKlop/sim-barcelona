from asyncio.windows_events import NULL
from http import HTTPStatus

from flask import Blueprint, Response, app, render_template
from server.logic.announcer import announcer
from server.logic import format_sse
from server.logic import do_the_thing

api = Blueprint('api', __name__, url_prefix='/api')

#main app html
@api.route('/')
def index():
    return render_template('api_index.html')

#button click
@api.route('/buttonclick')
def onButtonClick():
    do_the_thing()
    pass

#python call test
@app.route('/python_call_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


@api.route('/hello', methods=['GET'])
def hello():
    announcer.announce(format_sse('Hello, world!'))
    return 'Hello World!', HTTPStatus.OK

# @api.route('generateimage', methods=['GET'])
# def generateImgae(imgPath = NULL):
    
#     return;

@api.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')