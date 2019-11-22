# run.py

import os

from app import create_app
from flask_socketio import SocketIO

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
app.secret_key = 'randomString'
socketio = SocketIO(app)


if __name__ == '__main__':
   # app.run()
    socketio.run(app)
