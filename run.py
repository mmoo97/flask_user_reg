# run.py

import os
import time

from app import create_app
from flask_socketio import SocketIO
from flask import flash

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('user connect')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))


@socketio.on('user data')
def confirm(json, methods=['GET', 'POST']):
    print ('request received: ', str(json))

    try:
        fullname = json["fullname"]
        reason = json["reason"]
        username = json["username"]

        time_stamp = time.strftime("%m-%d-%Y_%H:%M:%S")
        directory = "flat_db/"
        complete_file_name = os.path.join(directory, time_stamp + "_" + username + ".txt")

        if not os.path.exists(directory):
            os.makedirs(directory)

        file = open(complete_file_name, "w")  # create time stamped file to be queued

        file.write(fullname + "\n")
        file.write(reason)

        file.close()
        socketio.emit("creating account")
    except Exception as e:
        print("Error in directory creation: ", e)
        socketio.emit("Account creation failed")


if __name__ == '__main__':
   # app.run()
    socketio.run(app)
