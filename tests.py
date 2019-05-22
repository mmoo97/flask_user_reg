# tests.py

import unittest

import flask
from flask import abort, url_for, g
from flask_testing import TestCase

from app import create_app


class TestBase(TestCase):

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        app = create_app('testing')
        return app

    def tearDown(self):
        """
        Will be called after every test
        """


class TestModels(TestBase):
    # TODO: make tests
    pass


class TestViews(TestBase):
    # TODO: make tests

    def test_index_view(self):
        """
        Test that homepage is accessible.
        """

        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)

        # with self.app.test_client() as c:
        #     rv = c.get('/')
        #     assert flask.session['REMOTE_USER'] == 'bobby'

    def test_page_resources(self):
        """
        Test that all resources load are found.
        """
        with self.app.test_request_context('/?redir=test'):
            assert flask.request.path == '/'
            c = flask.app.request.args['redir']
            assert c == 'test'

    # def test_logout_view(self):
    #     """
    #     Test that logout link is inaccessible without login
    #     and redirects to login page then to logout
    #     """
    #     target_url = url_for('auth.logout')
    #     redirect_url = url_for('auth.login', next=target_url)
    #     response = self.client.get(target_url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, redirect_url)\


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)


if __name__ == '__main__':
    unittest.main()
