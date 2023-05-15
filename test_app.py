from werkzeug.security import check_password_hash
from project.models import User
from project import create_app, db
from flask import current_app
import unittest
<< << << < HEAD
# Siddhant test 2
== == == =
>>>>>> > c59790389528bc04424a80c02ede44aec68b5afc


class TestWebApp(unittest.TestCase):
    def setUp(self):


<< << << < HEAD
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": 'sqlite://'})
== == == =
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": 'sqlite://'})
>>>>>> > 87067cc263a620dd1cf39478b18d578fec3c6f6c
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.appctx = self.app.app_context()  # test 2
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_homepage_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200

    def test_registration_form(self):
        response = self.client.get('/signup')
        assert response.status_code == 200

    def test_no_access_to_profile(self):
        # TODO: Check that non-logged-in user should be redirected to /login
        response = self.client.get('/profile',
                                   follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login'

    def test_register_user(self):
        response = self.client.post('/signup', data={
            'email': 'user@test.com',
            'name': 'test user',
            'password': 'test123'
        }, follow_redirects=True)
        assert response.status_code == 200
        # should redirect to the login page
        assert response.request.path == '/login'

        # verify that user can now login
        response = self.client.post('/login', data={
            'email': 'user@test.com',
            'password': 'test123'
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'test user' in html

    def test_hashed_passwords(self):
        response = self.client.post('/signup', data={
            'email': 'user@test.com',
            'name': 'test user',
            'password': 'test123'
        }, follow_redirects=True)
        assert response.status_code == 200
        # should redirect to the login page
        assert response.request.path == '/login'

        user = User.query.filter_by(email='user@test.com').first()
        assert user is not None
        assert check_password_hash(user.password, 'test123')

    def test_sql_injection(self):
        response = self.client.post('/signup', data={
            'email': 'user@test.com"; drop table user; -- ',
            'name': 'test user',
            'password': 'test123'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_xss_vulnerability(self):
        response = self.client.post('/signup', data={
            'email': 'user@test.com',
            'name': '<script> alert("Hello");</script>',
            'password': 'test123'
        }, follow_redirects=True)
        assert response.status_code == 200

        # verify that the user can now login
        response == self.client.post('/login', data={
            'email': 'user@test.com',
            'password': 'test123'
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert not '<script>' in html
# i added this comment - pridogs
# i added this comment - pridogs to dev
