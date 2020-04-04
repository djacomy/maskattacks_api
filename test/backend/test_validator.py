# -*- coding: utf-8 -*-

from validator.orga import check_address, check_organisation
from test.utils.mixins import BaseTest


class TestOrga(BaseTest):
    fixtures = ["users.json", "refs.json"]

    def test_chech_address(self):

        params = {
            "street": "30 rue du paradis",
            "zipcode": "34344",
            "city": "le paradis",
        }
        obj, errors  = check_address(params)
        self.assertEqual(obj, {
            "street": "30 rue du paradis",
            "zipcode": "34344",
            "city": "le paradis",
            "lon": None,
            "lat": None
        })
        self.assertEqual(errors, [])

    def test_chech_address_errors(self):

        params = {
            "street": "30 rue du paradis",
            "city": "le paradis",
        }
        obj, errors = check_address(params)

        self.assertEqual(obj, {
            "street": "30 rue du paradis",
            "zipcode": None,
            "city": "le paradis",
            "lon": None,
            "lat": None
        })
        self.assertEqual(errors, [{'code': 'FIELD_REQUIRED', 'message': 'zipcode of address is required'}])

    def test_check_orga_with_provider(self):
        params = {
            "name": "Hôpital du Paradis",
            "role": "man",
            "status": "running",
            "availability": "midtime",
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
             },
            "manufactor": {
                "type": "Couturier",
                "capacity": "Faible",
                "skill_level": "Confirmé",
                "quality_need": "Qualité Max",
                "contract_type": "Bénévole"
            }
        }
        obj, errors = check_organisation(params)
        self.assertEqual(obj, {
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
        })
        self.assertEqual(errors, [])

    def test_check_orga_without_provider(self):
        params = {
            "name": "Hôpital du Paradis",
            "role": "man",
            "status": "running",
            "availability": "midtime",
        }
        obj, errors = check_organisation(params)
        self.assertEqual(obj, {
            "name": "Hôpital du Paradis",
            "role": 7,
            "status": 1,
            "availability": 4,
            'address': None,
            'customer': None,
            'manufactor': None,
            'provider': None,
            'transporter': None
        })
        self.assertEqual(errors,
                         [{'code': 'FIELD_REQUIRED', 'message': 'user of organisation is required'},
                          {'code': 'FIELD_REQUIRED', 'message': 'address of organisation is required'},
                          {'code': 'FIELD_REQUIRED', 'message': 'manufactor of organisation is required'}])

    def test_check_orga_with_no_role(self):
        params = {
            "name": "Hôpital du Paradis",
            "status": "running",
            "availability": "midtime",
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
            },
            "manufactor": {
                "type": "Couturier",
                "capacity": "Faible",
                "skill_level": "Confirmé",
                "quality_need": "Qualité Max",
                "contract_type": "Bénévole"
            }
        }
        obj, errors = check_organisation(params)
        self.assertEqual(obj, {
            "name": "Hôpital du Paradis",
            "role": None,
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
            "manufactor": {
                "type": "Couturier",
                "capacity": "Faible",
                "skill_level": "Confirmé",
                "quality_need": "Qualité Max",
                "contract_type": "Bénévole"
            },
            'provider': None,
            'transporter': None
        })
        self.assertEqual(errors,
                         [{'code': 'FIELD_REQUIRED',
                           'message': 'role of organization is required'}
                          ])




