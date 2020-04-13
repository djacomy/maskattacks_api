import json

import unittest
from test.utils.mixins import BaseTest, BaseAuthMixin


class TestProduct(BaseTest, BaseAuthMixin):
    maxDiff = None
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json']

    def test_get_products(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/products'
        response = self.get(url, token, {"page": 2, "size": 3})
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.json)
        self.assertEqual(3, len(response.json["products"]))
        self.assertEqual(response.json["products"],
                         [{'id': 1003, 'reference': 'MEFP2', 'type': 'final',
                           'libelle': 'Mask efp2',
                           'materials': [{'id': 1000, 'reference': 'SAXXXY', 'type': "materials",
                                          'libelle': 'Tissus de 50m2', 'count': 5},
                                         {'id': 1002, 'reference': 'SAXXYY', 'type': "materials",
                                          'libelle': 'Elastique pour mask', 'count': 5}]},
                          {'id': 1004, 'reference': 'MTOILE', 'type': 'final', 'libelle': 'Mask toile',
                           'materials': []},
                          {'id': 1005, 'reference': 'MEFP2+', 'type': 'final', 'libelle': 'Super Mask efp2',
                           'materials': [{'id': 1001, 'reference': 'SAXXXZ',
                                          'type': "materials", 'libelle': 'Tissus de 30m2', 'count': 4},
                                         {'id': 1002, 'reference': 'SAXXYY', 'type': "materials",
                                          'libelle': 'Elastique pour mask', 'count': 5}
                                         ]
                           }
                          ])

    def test_create_product(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/products'
        response = self.post(url, token, {"product_type": "materials",
                                          "reference": "ABCDE",
                                          "libelle":"Mon super produit"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'id': 1, 'reference': 'ABCDE',
                          'type': 'materials',
                          'libelle': 'Mon super produit'})

    def test_get_product(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/products/SAXXXY'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'id': 1000, 'reference': 'SAXXXY',
                          'type': 'materials',
                          'libelle': 'Tissus de 50m2'})

    def test_update_product_error(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/products/SAXXXY'
        response = self.put(url, token, {"materials": [{"reference": "xxxxx", "count": 5}]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {'errors': [{'code': 'BAD_FINAL_PRODUCT',
                                      'message': 'SAXXXY is not a final product.'},
                                     {'code': 'BAD_MATERIAL_PRODUCT',
                                      'message': 'xxxxx is not a material product.'}]})

    def test_update_product(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/products/MTOILE'
        response = self.put(url, token, {"materials": [{"reference": "SAXXXZ", "count": 5},
                                                       {"reference": "SAXXYY", "count": 5}]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'id': 1004,
                          'libelle': 'Mask toile',
                          'materials': [{'count': 4,
                                         'id': 1001,
                                         'libelle': 'Tissus de 30m2',
                                         'reference': 'SAXXXZ',
                                         'type': 'materials'},
                                        {'count': 5,
                                         'id': 1002,
                                         'libelle': 'Elastique pour mask',
                                         'reference': 'SAXXYY',
                                         'type': 'materials'}],
                          'reference': 'MTOILE',
                          'type': 'final'}
                         )


if __name__ == '__main__':
    unittest.main()
