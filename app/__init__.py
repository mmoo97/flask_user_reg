# app/__init__.py

# local imports
from __future__ import print_function

import os
import os.path
import sys
import time
import datetime
import subprocess
# third-party imports
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_bootstrap import Bootstrap


def create_app(config_name):

    app = Flask(__name__)
    Bootstrap(app)

    global return_url
    return_url = ''

    @app.route('/', methods=['GET', 'POST'])
    def index():

        user = request.remote_user

        if request.method == 'GET':

            global return_url

            if "redir" in request.args:
                return_url = request.args.get("redir") or "/pun/sys/dashboard"

            return render_template("auth/SignUp.html", user=user)

        if request.method == 'POST':

            name = request.form['name']

            if name != "":

                return redirect(url_for('success', username=str(user), fullname=name))

            else:
                return render_template("auth/SignUp.html", user=user)

    @app.route('/success/<username>/<fullname>')
    def success(username, fullname):

        global return_url
        print(username, fullname, return_url, file=sys.stdout)

        # Deliver arguments to script.
        tempString = 'ssh ohpc "sudo /opt/ohpc_user_create/user_create ' + username + " " + fullname + '"'
        print(tempString, file=sys.stdout)

        try:

            time_stamp = time.strftime("%m-%d-%Y--%H:%M:%S")
            directory = "/var/www/ood/register/flask_user_reg/app/flat_db"
            complete_file_name = os.path.join(directory, time_stamp + ".txt")

            if not os.path.exists(directory):
                os.makedirs(directory)

            file = open(complete_file_name, "w")
            file.write(fullname)
            file.close()
            return redirect(return_url, 302)

        except:
            flash("Registration Failed")
            return redirect(return_url)


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
