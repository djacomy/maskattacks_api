# -*- coding: utf-8 -*-

from maskattacks.repository import orga as orga_repo, product as product_repo
from tests.utils.mixins import BaseTest


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


class TestStock(BaseTest):
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json']

    def test_list_product_references(self):
        obj = product_repo.list_product_references(1)
        self.assertEqual(obj,
                         [{'id': 1000, 'reference': 'SAXXXY', 'type': 'materials',
                           'libelle': 'Tissus de 50m2'},
                          {'id': 1001, 'reference': 'SAXXXZ', 'type': 'materials',
                           'libelle': 'Tissus de 30m2'},
                          {'id': 1002, 'reference': 'SAXXYY', 'type': 'materials',
                           'libelle': 'Elastique pour mask'},
                          {'id': 1003, 'reference': 'MEFP2', 'type': 'final',
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

    def test_list_product_references_page(self):
        obj = product_repo.list_product_references(2, 3)
        self.assertEqual(obj,
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

    def test_create_product_reference(self):
        obj = product_repo.create_product_reference(product_repo.ProductType.final,
                                                    "BLXXXX", "Blouse")

        product_repo.create_equivalence(obj, "SAXXXY", 5)
        product_repo.create_equivalence(obj, "SAXXYY", 5)
        self.assertTrue(isinstance(obj, product_repo.Product))

    def test_count_all_Stock(self):
        obj = product_repo.get_product_reference_by_reference("SAXXXY")
        product_repo.create_material_stock(obj, 25)
        product_repo.create_material_stock(obj, 10)
        obj = product_repo.get_product_reference_by_reference("SAXXYY")
        product_repo.create_material_stock(obj, 10)
        obj = [it for it in product_repo.count_all_stocks_by_reference_and_type().items]
        self.assertEqual(obj,
                         [('SAXXYY',  product_repo.ProductType.materials, 10),
                          ('SAXXXY',  product_repo.ProductType.materials, 35)]
                         )

    def test_count_stock(self):
        obj = product_repo.get_product_reference_by_reference("SAXXXY")
        product_repo.create_material_stock(obj, 25)
        product_repo.create_material_stock(obj, 10)

        obj = product_repo.count_stock_by_reference("SAXXXY")
        self.assertEqual(35, obj)

        obj = product_repo.list_stocks_by_reference("SAXXXY")
        self.assertEqual([(it.product.reference, it.count)for it in  obj.all()],
                         [('SAXXXY', 25), ('SAXXXY', 10)])

    def test_check_stock_error_1(self):
        obj = product_repo.get_product_reference_by_reference("SAXXXY")
        product_repo.create_material_stock(obj, 35)
        obj = product_repo.get_product_reference_by_reference("SAXXXY")
        product_repo.create_material_stock(obj, 10)

        obj = product_repo.get_product_reference_by_reference("MEFP2")
        with self.assertRaises(product_repo.ProductException):
            product_repo.check_kit_stock_creation(obj, 10)

    def test_check_stock_error_2(self):
        obj = product_repo.get_product_reference_by_reference("SAXXXY")
        product_repo.create_material_stock(obj, 25)

        obj = product_repo.get_product_reference_by_reference("MEFP2")
        with self.assertRaises(product_repo.ProductException) as ctx:
            product_repo.check_kit_stock_creation(obj, 10)

    def test_check_kit_stock(self):
        obj = product_repo.get_product_reference_by_reference("SAXXXY")
        product_repo.create_material_stock(obj, 50)
        obj = product_repo.get_product_reference_by_reference("SAXXYY")
        product_repo.create_material_stock(obj, 50)

        obj = product_repo.get_product_reference_by_reference("MEFP2")
        self.assertTrue(product_repo.check_kit_stock_creation(obj, 10))

    def test_create_kit_stock(self):
        obj = product_repo.get_product_reference_by_reference("SAXXXY")
        product_repo.create_material_stock(obj, 55)
        obj = product_repo.get_product_reference_by_reference("SAXXYY")
        product_repo.create_material_stock(obj, 50)

        obj = product_repo.get_product_reference_by_reference("MEFP2")
        self.assertTrue(product_repo.create_kit_stock(obj, 10))

        obj = [it for it in product_repo.count_all_stocks_by_reference_and_type().items]
        self.assertEqual(obj,
                         [("MEFP2", product_repo.ProductType.kit, 10),
                          ('SAXXXY', product_repo.ProductType.materials, 5)])


class TestDeliveryItem(BaseTest):
    fixtures = ["refs.json", "users.json", "orga.json", 'product.json', 'stock.json']

    def test_create_kit_delivery_stock(self):

        obj = product_repo.get_product_reference_by_reference("MEFP2+")
        manufactor = orga_repo.get_organisation(6)
        product_repo.create_kit_delivery_stock(obj, 40, manufactor)

        obj1 = [it for it in product_repo.count_all_stocks_by_reference_and_type().items]
        self.assertEqual(obj1, [('MEFP2+', product_repo.ProductType.kit, 10)])
        obj2 = [it for it in product_repo.count_all_delivery_by_reference_and_type().items]
        self.assertEqual(obj2, [('MTOILE', "Couturier 2", product_repo.ProductType.kit,
                                  product_repo.StatusType.submitted, 120),
                                ('MEFP2+', 'Couturier 1', product_repo.ProductType.kit,
                                 product_repo.StatusType.submitted, 40)])

    def test_create_final_delivery_stock(self):
        obj = product_repo.get_product_reference_by_reference("MEFP2+")
        manufactor = orga_repo.get_organisation(6)
        product_repo.create_final_delivery_stock(obj, 40, manufactor)

        obj1 = [it for it in product_repo.count_all_stocks_by_reference_and_type().items]
        self.assertEqual(obj1, [('MEFP2+', product_repo.ProductType.kit, 50)])
        obj2 = [it for it in product_repo.count_all_delivery_by_reference_and_type().items]
        self.assertEqual(obj2, [('MTOILE', "Couturier 2", product_repo.ProductType.kit,
                                 product_repo.StatusType.submitted, 120),
                                ('MEFP2+', 'Couturier 1', product_repo.ProductType.final,
                                 product_repo.StatusType.submitted, 40)
                                ])

    def test_create_delivery_batch(self):

        obj = product_repo.get_deliveryitem_by_reference_and_type("MTOILE", "kit")
        product_repo.generate_batch_from_delivery_item(obj, 40)
        obj = [it for it in product_repo.list_all_batches().items]
        expected_result = [(1, 'Couturier 2', product_repo.StatusType.submitted, 40),
                           (2, 'Couturier 2', product_repo.StatusType.submitted, 40),
                           (3, 'Couturier 2', product_repo.StatusType.submitted, 40)]

        for i, item in enumerate(expected_result):
            self.assertEqual(str, type(obj[i][0]))
            self.assertEqual(item[1], obj[i][1])
            self.assertEqual(item[2], obj[i][2])
            self.assertEqual(item[3], obj[i][3])
