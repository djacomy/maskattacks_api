# -*- coding: utf-8 -*-

from repository import orga as orga_repo
from repository import product as product_repo
from test.utils.mixins import BaseTest


def dump(obj):
    for k, v in obj.items():
        if isinstance(v, dict):
            dump(v)
        else:
            try:
                print(k, v)
            except UnicodeDecodeError:
                print(k, v.decode('iso-8859-1'))


class TestOrga(BaseTest):
    fixtures = ["refs.json",  "users.json", "orga.json"]

    def test_get_provider(self):
        obj = orga_repo.get_provider(1000).first()
        self.assertEqual(obj.json, {'type': 'fm', 'subtype': 'fta'})

    def test_create_manufactor_orga(self):
        params = {
            "name": "Hôpital du Paradis",
            "role": 7,
            "status": 1,
            "availability": 4,
            "user": {
                "email": "jim@example.fr",
                "firstname": "Jimmy",
                "lastname": "Le Duc",
                "password": "jimmyleduc"
            },
            "address": {
                "street": "30 rue du paradis",
                "zipcode": "34344",
                "city": "le paradis",
                "lon": None,
                "lat": None
            },
            'customer': None,
            "manufactor": {'type': 11,
                           'capacity': 13,
                           'skill_level': 16,
                           'quality_need': 18,
                           'contract_type': 22},
            'provider': None,
            'transporter': None
        }
        obj = orga_repo.create_organization(params)
        self.assertEqual(1, obj.id)


class TestProduct(BaseTest):
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json']

    def test_create_product_reference(self):
        obj = product_repo.create_product_reference(product_repo.ProductType.final,
                                                    "BLXXXX", "Blouse")

        product_repo.create_equivalence(obj, "SAXXXY", 5)
        product_repo.create_equivalence(obj, "SAXXYY", 5)
        self.assertTrue(isinstance(obj, product_repo.Product))

    def test_count_all_Stock(self):
        product_repo.create_material_stock("SAXXXY", 25)
        product_repo.create_material_stock("SAXXXY", 10)
        product_repo.create_material_stock("SAXXYY", 10)
        obj = product_repo.count_all_stocks_by_reference_and_type()
        self.assertEqual(obj,
            [('SAXXYY', product_repo.ProductType.materials, 10),
             ('SAXXXY', product_repo.ProductType.materials, 35)]
        )

    def test_count_stock(self):
        product_repo.create_material_stock("SAXXXY", 25)
        product_repo.create_material_stock("SAXXXY", 10)
        obj = product_repo.count_stock_by_reference("SAXXXY")
        self.assertEqual(35, obj)

        obj = product_repo.list_stocks_by_reference("SAXXXY")
        self.assertEqual([(it.product.reference, it.count)for it in  obj.all()],
                         [('SAXXXY', 25), ('SAXXXY', 10)])

    def test_check_stock_error_1(self):
        product_repo.create_material_stock("SAXXXY", 35)
        product_repo.create_material_stock("SAXXXY", 10)

        prod = product_repo.get_product_reference_by_reference("MEFP2")
        with self.assertRaises(product_repo.ProductException):
            product_repo.check_kit_stock_creation("MEFP2", 10)

    def test_check_stock_error_2(self):
        product_repo.create_material_stock("SAXXXY", 25)

        prod = product_repo.get_product_reference_by_reference("MEFP2")
        with self.assertRaises(product_repo.ProductException) as ctx:
            product_repo.check_kit_stock_creation("MEFP2", 10)

    def test_check_kit_stock(self):
        product_repo.create_material_stock("SAXXXY", 50)
        product_repo.create_material_stock("SAXXYY", 50)

        prod = product_repo.get_product_reference_by_reference("MEFP2")
        self.assertTrue(product_repo.check_kit_stock_creation("MEFP2", 10))

    def test_create_kit_stock(self):
        product_repo.create_material_stock("SAXXXY", 55)
        product_repo.create_material_stock("SAXXYY", 50)

        prod = product_repo.get_product_reference_by_reference("MEFP2")
        self.assertTrue(product_repo.create_kit_stock("MEFP2", 10))

        obj = product_repo.count_all_stocks_by_reference_and_type()
        self.assertEqual(obj,
                         [("MEFP2", product_repo.ProductType.kit, 10),
                          ('SAXXXY', product_repo.ProductType.materials, 5)])
