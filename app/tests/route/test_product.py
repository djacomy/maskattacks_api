import unittest

from maskattacks.repository import product as prod_repo
from tests.utils.mixins import BaseTest, BaseAuthMixin


class TestProduct(BaseTest, BaseAuthMixin):
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json']

    def test_get_products(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/products'
        response = self.get(url, token, {"page": 2, "size": 3})
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json)
        self.assertEqual(6, response.json["total"])
        self.assertEqual(2, response.json["page"])
        self.assertEqual(3, response.json["size"])
        self.assertEqual(response.json["results"],
                         [{'reference': 'MEFP2', 'type': 'final',
                           'libelle': 'Mask efp2',
                           'materials': [{'reference': 'SAXXXY', 'type': "materials",
                                          'libelle': 'Tissus de 50m2', 'count': 5},
                                         {'reference': 'SAXXYY', 'type': "materials",
                                          'libelle': 'Elastique pour mask', 'count': 5}]},
                          {'reference': 'MTOILE', 'type': 'final', 'libelle': 'Mask toile',
                           'materials': []},
                          {'reference': 'MEFP2+', 'type': 'final', 'libelle': 'Super Mask efp2',
                           'materials': [{'reference': 'SAXXXZ',
                                          'type': "materials", 'libelle': 'Tissus de 30m2', 'count': 4},
                                         {'reference': 'SAXXYY', 'type': "materials",
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
                         {'reference': 'ABCDE',
                          'type': 'materials',
                          'libelle': 'Mon super produit'})

    def test_get_product(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/products/SAXXXY'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'reference': 'SAXXXY',
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
                         {'libelle': 'Mask toile',
                          'materials': [{'count': 4,
                                         'libelle': 'Tissus de 30m2',
                                         'reference': 'SAXXXZ',
                                         'type': 'materials'},
                                        {'count': 5,
                                         'libelle': 'Elastique pour mask',
                                         'reference': 'SAXXYY',
                                         'type': 'materials'}],
                          'reference': 'MTOILE',
                          'type': 'final'}
                         )


class TestStock(BaseTest, BaseAuthMixin):
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json', 'stock2.json']

    def test_get_stocks(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks'
        response = self.get(url, token, {"page": 1, "size": 3})
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json)

        self.assertEqual(response.json,
                         {'total': 3,
                          'page': 1,
                          'size': 3,
                          'results': [{'reference': 'MEFP2+', 'type': 'kit', 'count': 50},
                                     {'reference': 'SAXXYY', 'type': 'materials', 'count': 200},
                                     {'reference': 'SAXXXY', 'type': 'materials', 'count': 200}]})

    def test_create_material_stock(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks'
        response = self.post(url, token, {"reference": "SAXXYY", "count": 23})
        self.assertEqual(response.status_code, 200)
        obj = prod_repo.count_stock_by_reference("SAXXYY")
        self.assertEqual(223, obj)

    def test_create_kit_stock_not_enough(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks'
        response = self.post(url, token, {"reference": "MEFP2", "count": 100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {'errors': [{'code': 'NOT_ENOUGH_STOCK', 'message': 'Not enough stock for reference SAXXXY'},
                                     {'code': 'NOT_ENOUGH_STOCK', 'message': 'Not enough stock for reference SAXXYY'}]})

    def test_create_kit_stock(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks'
        response = self.post(url, token, {"reference": "MEFP2", "count": 10})
        self.assertEqual(response.status_code, 200)
        obj = prod_repo.count_stock_by_reference("MEFP2")
        self.assertEqual(10, obj)

    def test_get_stock(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks/SAXXYY'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'reference': 'SAXXYY', 'type': 'materials', 'count': 200})

    def test_get_unknown_stock(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/stocks/SAXXY'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'errors': [
            {"code": "UNKNOWN_RESOURCE", "message": "Unknown ressource"}
        ]})


class TestDeliveryItem(BaseTest, BaseAuthMixin):
    maxDiff = None
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json', 'stock2.json']

    def test_get_deliveyitems(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/deliveryitems'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json)
        self.assertEqual(response.json,
                         {'total': 3, 'page': 1, 'size': 10,
                          'results': [{'reference': 'MTOILE', 'manufactor': 'Couturier 2',
                                       'type': 'kit', 'status': 'submitted', 'count': 120},
                                      {'reference': 'MEFP2', 'manufactor': 'Couturier 1',
                                       'type': 'final', 'status': 'submitted', 'count': 115},
                                      {'reference': 'MEFP2', 'manufactor': 'Couturier 1',
                                       'type': 'kit', 'status': 'submitted', 'count': 120}]})

    def test_create_kit_delivery(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/deliveryitems'
        response = self.post(url, token, {"reference": "MEFP2+",
                                          "manufactor_vid": 6,
                                          "delivery_type": "kit",
                                          "count": 23})
        self.assertEqual(response.status_code, 204)
        obj = prod_repo.count_delivery_by_reference_and_type("MEFP2+", prod_repo.ProductType.kit)
        self.assertEqual(23, obj)

    def test_create_final_delivery(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/deliveryitems'
        response = self.post(url, token, {"reference": "MEFP2+",
                                          "manufactor_vid": 6,
                                          "delivery_type": "final",
                                          "count": 23})

        self.assertEqual(response.status_code, 204)
        obj = prod_repo.count_delivery_by_reference_and_type("MEFP2+", prod_repo.ProductType.final)
        self.assertEqual(23, obj)

    def test_create_kit_delivery_bad_manufactor(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/deliveryitems'
        response = self.post(url, token, {"reference": "MEFP2",
                                          "manufactor_vid": 4,
                                          "delivery_type": "final",
                                          "count": 100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {'errors': [{'code': 'NOT_A_MANUFACTOR', 'message': '4 is not a manufactor'}]})

    def test_get_deliveryitem(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/deliveryitems/MEFP2'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'reference': 'MEFP2',
                                         'deliveries': [
                                             {'manufactor': 'Couturier 1', 'type':'kit',
                                              'status': 'submitted', 'count': 120},
                                             {'manufactor': 'Couturier 1', 'type': 'final',
                                              'status': 'submitted', 'count': 115}
                                         ]})

    def test_get_unknown_deliveryitem(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/deliveryitems/SAXXY'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'errors': [
            {"code": "UNKNOWN_RESOURCE", "message": "Unknown ressource"}
        ]})


class TestBatch(BaseTest, BaseAuthMixin):
    maxDiff = None
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json', 'stock2.json']

    def test_get_batches(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json)
        self.assertEqual(response.json,
                         {'total': 6, 'page': 1, 'size': 10,
                          'results': [{'reference': 'batch1',
                                       'status': 'submitted',
                                       'product_reference': 'MEFP2',
                                       'delivery_type': "kit",
                                       'destination': 'Couturier 1',
                                       'transporter': None, 'count': 50},
                                      {'reference': 'batch2', 'status': 'submitted',
                                       'product_reference': 'MEFP2',
                                       'delivery_type': "kit",
                                       'destination': 'Couturier 1', 'transporter': None,
                                       'count': 50},
                                      {'reference': 'batch3', 'status': 'submitted',
                                       'product_reference': 'MEFP2',
                                       'delivery_type': "kit",
                                       'destination': 'Couturier 1', 'transporter': None,
                                       'count': 20},
                                      {'reference': 'batch4', 'status': 'submitted',
                                       'product_reference': 'MEFP2',
                                       'delivery_type': "final",
                                       'destination': 'Entreprise de textile',
                                       'transporter': None, 'count': 50},
                                      {'reference': 'batch5', 'status': 'submitted',
                                       'product_reference': 'MEFP2',
                                       'delivery_type': "final",
                                       'destination': 'Entreprise de textile',
                                       'transporter': None, 'count': 50},
                                      {'reference': 'batch6', 'status': 'submitted',
                                       'product_reference': 'MEFP2',
                                       'delivery_type': "final",
                                       'destination': 'Entreprise de textile',
                                       'transporter': None, 'count': 15}]})

    def test_create_batch(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches'
        response = self.post(url, token, {"reference": "MTOILE",
                                          "delivery_type": "kit",
                                          "batch_size": 23})
        self.assertEqual(response.status_code, 204)

    def test_create_batch_unknown_deliveryitem(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches'
        response = self.post(url, token, {"reference": "MTOILES",
                                          "delivery_type": "kit",
                                          "batch_size": 23})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {'errors': [{'code': 'UNKNOWN_RESOURCE', 'message': 'Unknown ressource'}]})

    def test_create_batch_already_done(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches'
        response = self.post(url, token, {"reference": "MEFP2",
                                          "delivery_type": "kit",
                                          "batch_size": 23})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {'errors': [{'code': 'DELIVERYITEM_ALREADY_EXPORTED',
                                      'message': 'Delivery item MEFP2-kit has been already exported.'}]})

    def test_get_batch(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches/batch1'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'reference': 'batch1',
                          'status': 'submitted',
                          'product_reference': 'MEFP2',
                          'delivery_type': 'kit',
                          'destination': 'Couturier 1',
                          'transporter': None,
                          'count': 50})

    def test_get_batch_unknown_resource(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/batches/batch'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {'errors': [{'code': 'UNKNOWN_RESOURCE', 'message': 'Unknown ressource'}]})


if __name__ == '__main__':
    unittest.main()
