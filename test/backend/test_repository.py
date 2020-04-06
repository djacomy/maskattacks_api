# -*- coding: utf-8 -*-

from repository.orga import create_organization, get_provider
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
        obj = get_provider(1).first()
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
        obj = create_organization(params)
        self.assertEqual(1, obj.id)
