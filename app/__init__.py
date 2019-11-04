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

global time_stamp


def create_app(config_name):
    app = Flask(__name__) # initialization of the flask app
    Bootstrap(app) # allowing app to use bootstrap

    global return_url
    return_url = ''

    class MainForm(FlaskForm): # class for the form itself
        fullname = StringField('Full Name: ', [validators.DataRequired(), ])
        reason = StringField('Reason for Requesting Account: ', [validators.DataRequired(), ])
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
            reason = form.reason.data
            form.fullname.data = '' # reset form data upon capture
            form.fullname.data = '' # reset form data upon capture

            return redirect(url_for('success', username=str(username), fullname=fullname, reason=reason))

        return render_template('auth/SignUp.html', form=form, user=username)

    @app.route('/success/<username>/<fullname>')
    def success(username, fullname, reason):

        global return_url
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

            file = open(complete_file_name, "w") # create time stamped file to be queued

            file.write(reason)

            file.close()
            return render_template("auth/request_recieved.html") # Todo: replace template with redirect
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
