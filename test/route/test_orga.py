from repository.orga import create_organization
from test.utils.mixins import BaseTest, BaseAuthMixin


class TestOrga(BaseTest, BaseAuthMixin):
    fixtures = ["users.json", "refs.json"]

    def test_create_orga(self):
        params = {
            "vid": 1,
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
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/organizations'
        response = self.post(url, token, params)
        self.assertEqual(response.status_code, 200)
        output = {"id": 1,
                  "vid": 1,
                  "role": "man",
                  "status": "running",
                  'availability': 'midtime',
                  'address':
                      {'city': 'le paradis',
                       'lat': None,
                       'lon': None,
                       'street': '30 rue du paradis',
                       'zipcode': '34344'
                       },
                  'data': {'capacity': 'low',
                           'contract_type': 'volonteer',
                           'skill_level': 'semipro',
                           'type': 'cou'
                           },
                  }
        self.assertEqual(response.json, output)

    def test_get_provider(self):
        params = {
            "vid": 2,
            "name": "Entreprise de textile",
            "role": 10,
            "status": 1,
            "availability": 4,
            "user": {
                "email": "rom@example.fr",
                "firstname": "Romain",
                "lastname": "Le Tartempion",
                "password": "romainletartampion"
            },
            "address": {
                "street": "30 rue des visiteurs",
                "zipcode": "54344",
                "city": "covid-19",
                "lon": None,
                "lat": None
            },
            'customer': None,
            "manufactor": None,
            'provider': {
                "type": 33,
                "subtype": 35,
            },
            'transporter': None
        }
        create_organization(params)

        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/organization/'
        response = self.post(url, token, params)
        self.assertEqual(response.status_code, 200)
        output = {"id": 1,
                  "vid": 2,
                  "role": "pro",
                  "status": "running",
                  'availability': 'midtime',
                  'address':
                      {
                          "street": "30 rue des visiteurs",
                          "zipcode": "54344",
                          "city": "covid-19",
                          "lon": None,
                          "lat": None
                      },
                  'data': {'type': 'fm',
                           'subtype': 'fta'},
                  }
        self.assertEqual(response.json, output)

