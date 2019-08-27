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


def create_app(config_name):

    app = Flask(__name__)
    Bootstrap(app)

    global return_url
    return_url = ''

    class MainForm(FlaskForm):
        fullname = StringField('Username: ', [validators.DataRequired(), ])
        submit = SubmitField('Submit')

    @app.route('/', methods=['GET', 'POST'])
    def index():

        user = request.remote_user

        username = False
        form = MainForm()
        if form.validate_on_submit():
            username = form.username.data
            form.username.data = ''
            return redirect(url_for('success', username=str(user), fullname=name))

        return render_template('auth/SignUp.html', form=form, user=user)

        # if request.method == 'GET':
        #
        #         global return_url
        #
        #         if "redir" in request.args:
        #             return_url = request.args.get("redir") or "/pun/sys/dashboard"
        #
        #         return render_template("auth/SignUp.html", user=user)
        #
        #     if request.method == 'POST':
        #
        #         name = request.form['name']
        #
        #         if name != "":
        #
        #             return redirect(url_for('success', username=str(user), fullname=name))
        #
        #         else:
        #             return render_template("auth/SignUp.html", user=user)

    @app.route('/success/<username>/<fullname>')
    def success(username, fullname):

        global return_url
        print(username, fullname, return_url, file=sys.stdout)

        # Deliver arguments to script.
        tempString = 'ssh ohpc "sudo /opt/ohpc_user_create/user_create ' + username + " " + fullname + '"'
        print(tempString, file=sys.stdout)

        try:

            subprocess.check_output([tempString], shell=True)
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
