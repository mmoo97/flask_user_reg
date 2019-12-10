    # app/__init__.py

# local imports
from __future__ import print_function

import os
import sys
import subprocess
import time

# third-party imports
from flask import Flask, redirect, url_for, request, render_template, flash, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, TextAreaField, validators
from flask_socketio import SocketIO

# global declarations


def create_app(config_name):
    app = Flask(__name__) # initialization of the flask app
    Bootstrap(app) # allowing app to use bootstrap

    global return_url
    return_url = ''

    @app.route('/', methods=['GET', 'POST']) # initial route to display the reg page
    def index():
        global return_url
        username = "mmoo97"

        if "redir" in request.args and return_url == "": # check for redir arg in url
            return_url = request.args.get("redir") or "/pun/sys/dashboard"

        return render_template('auth/SignUp.html', user=username)

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
