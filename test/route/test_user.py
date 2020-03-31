import json

import unittest
from model.user import User
from test.utils.mixins import BaseTest, BaseAuthMixin


class TestAuth(BaseTest):

    def test_login(self):
        params = {
            "email": 'joe@example.fr',
            "password": 'super-secret-password'
        }
        response = self.client.post(
            '/api/auth/login',
            json=params,
            content_type="application/json"

        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertIn("token", result)

    def test_signup(self):
        params = {
            "email": 'bill@example.fr',
            "password": 'super-secret-password'
        }
        response = self.client.post(
            '/api/auth/signup',
            json=params,
            content_type="application/json"

        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertIn("id", result)
        self.assertEqual(result["id"], '2')


class TestUser(BaseAuthMixin, BaseTest):

    def test_get_user(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/user/%d' % self.user_id
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'id': 1, 'username': 'joe'})

    def test_update_user(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/user/%d' % self.user_id
        response = self.put(url, token, {'username': "titi"})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'id': 1, 'username': 'titi'})

    def test_delete_user(self):
        params = {
            "email": 'bill@example.fr',
            "password": 'super-secret-password'
        }
        response = self.client.post(
            '/api/auth/signup',
            json=params,
            content_type="application/json"

        )
        self.assertEqual(response.status_code, 200)
        token = self.authenticate('bill@example.fr', 'super-secret-password')
        result = json.loads(response.data.decode('utf-8'))
        url = 'api/user/%d' % int(result["id"])
        response = self.delete(url, token)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(User.query.filter_by(email='bill@example.fr').first())



if __name__ == '__main__':
    unittest.main()
