from threading import Lock

from server import create_app
from server.logic import button

if __name__ == "__main__":
    lock = Lock()
    button.setup(lock)
    app = create_app()
    app.run(host='0.0.0.0', debug=False)
