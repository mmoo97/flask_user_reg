# app/__init__.py

# local imports
from __future__ import print_function

import os
import sys
import subprocess
import time

# third-party imports
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_socketio import SockerIO, send
from wtforms import StringField, SubmitField, validators

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils import dirsnapshot


global snap_before
global snap_after
global snap_diff
global observing
global time_stamp

observing = False


class MyHandler(FileSystemEventHandler): # Watchdog handler class to take action when observation requested
    def on_modified(self, event):

        global snap_before
        global snap_after
        global snap_diff
        global observing
        global time_stamp

        # print(event.src_path + " modified.")
        snap_after = dirsnapshot.DirectorySnapshot("/home/reggie/flat_db", True) # take post flat_db creation snapshot of the directory
        snap_diff = dirsnapshot.DirectorySnapshotDiff(snap_before, snap_after) # object to compare the initial snapshot with the final snapshot

        try:

            if ("/home/reggie/flat_db/" + time_stamp + ".done") in snap_diff.files_moved[0]: # check for timestamped string with .done extention in flat_db

                observing = False
                # print("YES!")
        except Exception as e:
            print(e)
        # print("Created: ", snap_diff.files_created)
        # print("Deleted: ", snap_diff.files_deleted)
        # print("Modified: ", snap_diff.files_modified)
        # print("Moved: ", snap_diff.files_moved)

    def on_created(self, event):

        print(event.src_path + " created.")


def create_app(config_name):
    app = Flask(__name__) # initialization of the flask app
    Bootstrap(app) # allowing app to use bootstrap
    socketio = SockerIO(app)

    @socketio.on('event')
    def handlEvent(evt):
        print('Event: ' + evt)
        send(evt, brodcast = true)

    if __name__== '__main__':
        socketio.run(app)



    global return_url
    return_url = ''

    class MainForm(FlaskForm): # class for the form itself
        fullname = StringField('Full Name: ', [validators.DataRequired(), ])
        submit = SubmitField('Submit')

    @app.route('/', methods=['GET', 'POST']) # initial route to display the reg page
    def index():
        global return_url
        username = request.remote_user

        if "redir" in request.args and return_url == "": # check for redir arg in url
            return_url = request.args.get("redir") or "/pun/sys/dashboard"

        fullname = False
        form = MainForm() # initialize form object
        if form.is_submitted():
            fullname = form.fullname.data
            form.fullname.data = '' # reset form data upon capture

            return redirect(url_for('success', username=str(username), fullname=fullname))

        return render_template('auth/SignUp.html', form=form, user=username)

    @app.route('/success/<username>/<fullname>')
    def success(username, fullname):

        global return_url
        global snap_before
        global observing
        global time_stamp
        print(username, fullname, return_url, file=sys.stdout)

        # Deliver arguments to script. (for local vagrant implementation)
        tempString = 'ssh ohpc "sudo /opt/ohpc_user_create/user_create ' + username + " " + fullname + '"'
        print(tempString, file=sys.stdout)

        try:
            # function to write out a flatdb with the name of the file being a timestamp and the content
            # of the file beieng blazerID the user submitted from the flask form (fullname)

            time_stamp = time.strftime("%m-%d-%Y_%H:%M:%S")
            directory = "/home/reggie/flat_db/"
            complete_file_name = os.path.join(directory, time_stamp + "_" + request.remote_user + ".txt")

            if not os.path.exists(directory):
                os.makedirs(directory)

            event_handler = MyHandler() # initialize handler
            observer = Observer() # initialize obsever to relay to handler
            observer.schedule(event_handler, path='/home/reggie/flat_db', recursive=True)
            observer.start()

            observing = True

            file = open(complete_file_name, "w") # create time stamped file to be queued
            file.write("Hey")

            # take an initial state snapshot of the db after file queued
            snap_before = dirsnapshot.DirectorySnapshot("/home/reggie/flat_db", True)

            while observing:
                # TODO: Update page ui element dynamically

                time.sleep(5)
            observer.stop()
            file.close()
            return render_template("errors/registration_failed.html") # Todo: replace template with redirect
            # return redirect(return_url, 302)

        except Exception as e:
            print(e)
            flash("Registration Failed. Please try again.") # show error message upon failure
            return redirect(url_for('index'))

    # misc page error catching

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app
