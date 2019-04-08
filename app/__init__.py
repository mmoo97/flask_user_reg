# app/__init__.py

# third-party imports
from flask import Flask, redirect, url_for, request
from flask import render_template

# local imports


def create_app(config_name):

    app = Flask(__name__)

    @app.route('/success/<name>')
    def success(name):
        return 'welcome new user %s' % name

    @app.route('/', methods=['GET'])
    def index():
        return render_template("auth/SignUp.html")

    @app.route('/', methods=['POST'])
    def SignUp():
        if request.method == 'POST':
            email = request.form['email']
            # make username from email
            # user = request.environ('REMOTE_USER')
            # user = request.remote_user.name
            # user = request.environ
            user = 'Mitchell'
            return redirect(url_for('success', name=user))

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
