import json

import unittest
from model.user import User
from test.utils.mixins import BaseTest, BaseAuthMixin


class TestStock(BaseAuthMixin, BaseTest):

    def test_get_stocks(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks/1'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, [{"id": 1, "provider": "toto", 'kit_type': "kit1", "count": 10}])

    def test_update_stock(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks/%d' % self.user_id
        response = self.put(url, token, {"id": 1, "provider": "toto", 'kit_type': "kit1", "count": 11})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {"id": 1, "provider": "toto", 'kit_type': "kit1", "count": 11})


if __name__ == '__main__':
    unittest.main()
