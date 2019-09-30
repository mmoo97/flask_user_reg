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
from wtforms import StringField, SubmitField, validators

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils import dirsnapshot


global snap_before
global snap_after
global snap_diff
global observing

observing = False


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):

        global snap_before
        global snap_after
        global snap_diff
        global observing

        # print(event.src_path + " modified.")
        snap_after = dirsnapshot.DirectorySnapshot("/home/reggie/flat_db", True)
        snap_diff = dirsnapshot.DirectorySnapshotDiff(snap_before, snap_after)

        try:

            if ("/home/reggie/flat_db/" + time_stamp + ".done") in snap_diff.files_moved:
                observing = False
                # print("YES!")
        except Exception as e:
            print(e)
            observing = False
            pass
        # print("Created: ", snap_diff.files_created)
        # print("Deleted: ", snap_diff.files_deleted)
        # print("Modified: ", snap_diff.files_modified)
        print("Moved: ", snap_diff.files_moved)

    def on_created(self, event):

        print(event.src_path + " created.")


def create_app(config_name):
    app = Flask(__name__) # initialization of the flask appo
    Bootstrap(app) # allowing app to use bootstrap

    global return_url
    return_url = ''

    class MainForm(FlaskForm): # class for the form itself
        fullname = StringField('Full Name: ', [validators.DataRequired(), ])
        submit = SubmitField('Submit')

    @app.route('/', methods=['GET', 'POST']) # initial route to display the reg page
    def index():
        global return_url
        user = request.remote_user

        if "redir" in request.args and return_url == "":
            return_url = request.args.get("redir") or "/pun/sys/dashboard"

        username = False
        form = MainForm()
        if form.is_submitted():
            username = form.fullname.data
            form.fullname.data = ''

            return redirect(url_for('success', username=str(user), fullname=username))

        return render_template('auth/SignUp.html', form=form, user=user)

    @app.route('/success/<username>/<fullname>')
    def success(username, fullname):

        global return_url
        global snap_before
        global observing
        print(username, fullname, return_url, file=sys.stdout)

        # Deliver arguments to script.
        tempString = 'ssh ohpc "sudo /opt/ohpc_user_create/user_create ' + username + " " + fullname + '"'
        print(tempString, file=sys.stdout)

        try:
            # function to write out a flatdb with the name of the file being a timestamp and the content
            # of the file beieng blazerID the user submitted from the flask form (fullname)

            time_stamp = time.strftime("%m-%d-%Y_%H:%M:%S")
            directory = "/home/reggie/flat_db/"
            complete_file_name = os.path.join(directory, time_stamp + ".txt")

            if not os.path.exists(directory):
                os.makedirs(directory)

            event_handler = MyHandler()
            observer = Observer()
            observer.schedule(event_handler, path='/home/reggie/flat_db', recursive=True)
            observer.start()

            observing = True

            file = open(complete_file_name, "w")
            file.write("Hey")

            snap_before = dirsnapshot.DirectorySnapshot("/home/reggie/flat_db", True)

            while observing:
                # TODO: While loop will go here

                time.sleep(5)
            observer.stop()
            file.close()
            return render_template("errors/registration_failed.html")
            # return redirect(return_url, 302)

        except Exception as e:
            print(e)
            flash("Registration Failed. Please try again.")
            return redirect(url_for('index'))

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
