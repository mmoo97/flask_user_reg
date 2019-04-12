# app/__init__.py

# local imports
import os

# third-party imports
from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_bootstrap import Bootstrap


def create_app(config_name):

    app = Flask(__name__)
    Bootstrap(app)

    @app.route('/success/<name>/<username>')
    def success(username, name):

        # TODO: Deliver arguments to script.

        tempString = 'sudo user_create ' + username + " " + name
        os.system("ssh ohpc " + tempString)

        # TODO: Make the success route back to cheaha.

        # return "Username: %s | Name: %s" % (username, name)

        return redirect("http://localhost:8080", 302)

    @app.route('/', methods=['GET'])
    def index():
        return render_template("auth/SignUp.html")

    @app.route('/', methods=['GET', 'POST'])
    def SignUp():

        name = request.form['name']
        if request.method == 'POST' and name != "":

            # TODO: Test remote_user string handling from apache server.
            user = request.environ('REMOTE_USER')
            # user = '*remote user*'

            return redirect(url_for('success', username=user, name=name))

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
