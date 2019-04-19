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
    # TODO:// test return URL. *Possibly make a success page before returning?*
    return_url = request.referrer # 'https://www.google.com/'

    @app.route('/success/<name>/<username>')
    def success(username, name):

        # TODO: Deliver arguments to script.

        tempString = 'sudo user_create ' + username + " " + name
        os.system("ssh ohpc " + tempString)

        # TODO: Make the success route back to cheaha.

        # return "Username: %s | Name: %s" % (username, name)

        return redirect(return_url, 302)

    @app.route('/', methods=['GET'])
    def index():

        # TODO:// test remote user variable

        user = request.remote_user

        # user = 'tom'

        return render_template("auth/SignUp.html", user=user)

    @app.route('/', methods=['GET', 'POST'])
    def SignUp():

        name = request.form['name']
        user = request.environ('REMOTE_USER')
        # user = 'tom'

        if request.method == 'GET':

            return render_template("auth/SignUp.html", user=user)

        if request.method == 'POST' and name != "":

            return redirect(url_for('success', username=user, name=name))

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
