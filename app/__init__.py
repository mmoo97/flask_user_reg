# app/__init__.py

# local imports
from __future__ import print_function

import os
import sys

# third-party imports
from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_bootstrap import Bootstrap


def create_app(config_name):

    app = Flask(__name__)
    Bootstrap(app)
    # TODO:// test return URL. *Possibly make a success page before returning?*
    global return_url
    return_url = ''

    @app.route('/success/<name>/<username>')
    def success(username, name):

        global return_url
        print(username, name,return_url, file=sys.stdout)
        # Deliver arguments to script.
        # tempString = 'sudo user_create ' + username + " " + name
        # os.system("ssh ohpc " + tempString)

        return redirect(return_url, 302)

    @app.route('/', methods=['GET'])
    def index():

        # TODO: Make url origin url.
        global return_url
        return_url = "http://example.com"

        user = request.remote_user

        return render_template("auth/SignUp.html", user=user, url=return_url)

    @app.route('/', methods=['GET', 'POST'])
    def SignUp():

        name = request.form['name']

        # TODO: Test to make sure remote_user is captured
        user = request.remote_user

        if request.method == 'GET':

            return render_template("auth/SignUp.html", user=user)

        if request.method == 'POST' and name != "":

            return redirect(url_for('success', username=str(user), name=name))

        else:
            return render_template("auth/SignUp.html", user=user)

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
