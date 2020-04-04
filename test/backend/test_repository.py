# -*- coding: utf-8 -*-

from repository.orga import create_organization
from test.utils.mixins import BaseTest


class TestOrga(BaseTest):
    fixtures = ["users.json", "refs.json"]

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
