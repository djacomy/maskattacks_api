import json

import unittest
from test.utils.mixins import BaseTest, BaseAuthMixin


class TestRequest(BaseAuthMixin, BaseTest):

    def test_get_requests(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/requests'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result,
                         {'requests': [{'id': 1, 'institution': 'Hopital de Quimper',
                                        'product_type': 'mask_efp2', 'count': '25',
                                        'pro': True, 'create_timestamp': '2020-03-20T20:00:00',
                                        'status': 'submitted'},
                                       {"id": 2, "institution": "Hopital de Quimper", 'product_type': "mask_toile",
                                        "count": "43", "pro": True,
                                        "create_timestamp": "2020-03-20T20:00:00", "status": "submitted"}
                                       ]})

    def test_post_request_empty_input(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/requests'
        response = self.post(url, token, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {'errors': ['institution is required', 'product_type is required',
                                     'count is required', 'pro is required']})

    def test_post_request_bad_product_type(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/requests'
        response = self.post(url, token, {"institution": "Hopital Bercy",
                                          "product_type": "toot",
                                          "pro": True,
                                          "count": 30})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {'errors': ['product_type requires value belonged mask_efp2,mask_chirurg,mask_toile']})

    def test_post_request(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/requests'
        response = self.post(url, token, {"institution": "Hopital Bercy",
                                          "product_type": "mask_chirurg",
                                          "pro": True,
                                          "count": 30})
        self.assertEqual(response.status_code, 200)
        for k, v in  {'count': 30,
                          'create_timestamp':  '2020-03-24T00:58',
                           'id': 2,
                           'institution': 'Hopital Bercy',
                           'pro': True,
                           'product_type': 'mask_chirurg',
                           'status': 'submitted'}.items():
            self.assertIn(k, response.json)
            if k != "create_timestamp":
                self.assertEqual(v, response.json[k])


class TestKits(BaseAuthMixin, BaseTest):

    def test_get_kits(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/kits'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result,
                         {'kits': [{'id': 1, 'request_id': 1, 'product_type':
                             'kit', 'origin': 'entrepot1', 'destination': 'couturier1', 'status': 'to_build'}]})

    def test_update_kit(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/kits/1'
        response = self.put(url, token, {"status": "to_deliver", "assignee": "toto"})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'id': 1, 'request_id': 1, 'product_type':
                                  'kit', 'origin': 'entrepot1', 'destination': 'couturier1',
                                  "status": "to_deliver", "assignee": "toto"})


class TestProtection(BaseAuthMixin, BaseTest):

    def test_get_protections_bad_item(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/protections/1'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'errors': 'Not a product'})

    def test_get_protections(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/protections/2'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))

        self.assertEqual(result,
                         [{'id': 2, 'request_id': 1, 'reference': 'XXXX234', 'product_type': 'mask_efp2',
                           'origin': 'couturier1', 'destination': 'entrepot1', 'status': 'wait'}])

    def test_update_protection(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/protections/2'
        response = self.put(url, token, {"status": "to_deliver", "assignee": "toto"})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result, {'id': 2, 'request_id': 1, 'reference': 'XXXX234', 'product_type': 'mask_efp2',
                                  'origin': 'couturier1', 'destination': 'entrepot1',
                                  "status": "to_deliver", "assignee": "toto"})


class TestBatch(BaseAuthMixin, BaseTest):

    def test_get_batches(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual({"batches": []},  result)

    def test_post_batches_not_the_same_destination(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches'
        response = self.post(url, token, {"products": [3, 2]})
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual({'error': 'Not the same destination'},  result)

    def test_post_batches(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches'
        response = self.post(url, token, {"products": [3, 4]})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))

        for k, v in {'id': 0, 'create_timestamp': '2020-03-24T01:29:%i',
                      'destination': 'Hopital de Quimper', 'status': 'submitted'}.items():
            self.assertIn(k, result)
            if k != "create_timestamp":
                self.assertEqual(v, result[k])


if __name__ == '__main__':
    unittest.main()
