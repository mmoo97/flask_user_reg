# app/__init__.py

# third-party imports
from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_bootstrap import Bootstrap

# local imports


def create_app(config_name):

    app = Flask(__name__)
    Bootstrap(app)

    @app.route('/success/<name>/<username>')
    def success(username, name):
        # TODO: Make the success route back to cheaha.

        return "Username: %s | Name: %s" % (username, name)

    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html")
        # return redirect("http://localhost:8080")

    @app.route('/', methods=['POST'])
    def SignUp():

        name = request.form['name']

        if request.method == 'POST' and name != "":

            # TODO: Test remote_user string handling from apache server.
            # user = request.environ('REMOTE_USER')
            # user = request.remote_user.name
            user = "*remote_user*"

            # TODO: Deliver arguments to script.

            return redirect(url_for('success', name=name, username=user))

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
