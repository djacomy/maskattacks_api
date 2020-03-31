import unittest
import json

from model.abc import db
from model import User
from server import server


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()
        user = User('joe@example.fr', 'super-secret-password', 'joe')
        db.session.add(user)
        db.session.commit()
        cls.user_id = user.id
        server.config['TESTING'] = True
        cls.client = server.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.rollback()
        db.drop_all()

    @classmethod
    def tearDown(cls):
        db.session.rollback()


class BaseAuthMixin(object):

    def authenticate(self, email, password):
        response = self.client.post(
            '/api/auth/login',
            json={'email': email, 'password': password},
            content_type="application/json"

        )

        if response.status_code != 200:
            raise Exception("Invalide user")
        result = json.loads(response.data.decode('utf-8'))
        return result["token"]

    def get(self, url, token, params=None):

        return self.client.get(
            url,
            data=params,
            headers={'Authorization': 'Bearer ' + token}
        )

    def post(self, url, token, params=None):

        return self.client.post(
            url,
            data=params,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
        )

    def put(self, url, token, params=None):
        return self.client.put(
            url,
            json=params,
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
        )

    def delete(self, url, token):
        return self.client.delete(
            url,
            headers={'Authorization': 'Bearer ' + token}
        )


