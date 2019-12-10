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


def check_dir(user, interval):
    """
    :param user: (string) username to check for in DB.
    :param interval: (int) Frequency to check in seconds.
    :return: (boolean) if account has been registered.
    """
    seconds = 0

    while seconds < 600:
        querystring = "_" + user + ".done"

        for filename in os.listdir("flat_db/"):
            if filename.endswith(querystring):
                return True
        time.sleep(interval)
        seconds = seconds + interval

    return False


@socketio.on('user connect')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    username = json["user"]
    print('User ' + username + ' connected.')


@socketio.on('user data')
def ingest_data(json, methods=['GET', 'POST']):
    print ('Queue request received: ', str(json))

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
        print ('User ' + username + ' added to queue')
        socketio.emit("creating account")

    except Exception as e:
        print("Error in directory creation: ", e)
        socketio.emit("Account creation failed")


@socketio.on("validate creation")
def creation_confirmation(json, methods=['GET', 'POST']):
    username = json["username"]

    if check_dir(username, 10):
        print ('Account successfully created for ' + username)
        socketio.emit("Account created")
    else:
        socketio.emit("Account creation failed")


if __name__ == '__main__':
   # app.run()
    socketio.run(app)
