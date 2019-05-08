# app/__init__.py

# local imports
from __future__ import print_function

import os
import sys
import subprocess

# third-party imports
from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_bootstrap import Bootstrap


def create_app(config_name):

    app = Flask(__name__)
    Bootstrap(app)

    global return_url
    return_url = ''

    @app.route('/success/<name>/<username>')
    def success(username, name):

        global return_url
        print(username, name, return_url, file=sys.stdout)

        # Deliver arguments to script.
        tempString = 'ssh ohpc "sudo /opt/ohpc_user_create/user_create ' + username + ' \'' + name + '\'"'
        print(tempString, file=sys.stdout)

        output = subprocess.check_output([tempString], shell=True)

        print(output.split('\n')[7], file=sys.stdout)

        return redirect('/pun/sys/dashboard', 302)

    @app.route('/')
    def index():

        global return_url
        return_url = request.args.get("redir")[0] or "/pun/sys/dashboard"

        user = request.remote_user

        return redirect(url_for("SignUp", user=user))

    @app.route('/thing/', methods=['GET', 'POST'])
    def SignUp():

        user = request.remote_user

        if request.method == 'GET':

            return render_template("auth/SignUp.html", user=user)

        if request.method == 'POST':

            name = request.form['name']

            if name != "":

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
