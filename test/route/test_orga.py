from repository.orga import create_organization
from repository.orga import get_organisation
from test.utils.mixins import BaseTest, BaseAuthMixin


class TestOrga(BaseTest, BaseAuthMixin):
    maxDiff = None
    fixtures = ["users.json", "refs.json", "orga.json"]

    def test_get_references(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/references'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {
                             "orga_status": [
                                 {
                                     "code": "running",
                                     "libelle": "En Cours de Traitement"
                                 },
                                 {
                                     "code": "active",
                                     "libelle": "Actif dans le circuit"
                                 },
                                 {
                                     "code": "suspend",
                                     "libelle": "Paused"
                                 },
                                 {
                                     "code": "rejected",
                                     "libelle": "Rejeté"
                                 }
                             ],
                             "orga_availability": [
                                 {
                                     "code": "midtime",
                                     "libelle": "Mi-Temps"
                                 },
                                 {
                                     "code": "fulltime",
                                     "libelle": "Plein Temps"
                                 },
                                 {
                                     "code": "na",
                                     "libelle": "Non Applicable"
                                 }
                             ],
                             "orga_role": [
                                 {
                                     "code": "man",
                                     "libelle": "Manufact"
                                 },
                                 {
                                     "code": "tra",
                                     "libelle": "Transport"
                                 },
                                 {
                                     "code": "cus",
                                     "libelle": "Customer"
                                 },
                                 {
                                     "code": "pro",
                                     "libelle": "Provider"
                                 }
                             ],
                             "manufactor_type": [
                                 {
                                     "code": "cou",
                                     "libelle": "Couturier"
                                 },
                                 {
                                     "code": "print3d",
                                     "libelle": "Impresseur3D"
                                 }
                             ],
                             "manufactor_capacity": [
                                 {
                                     "code": "low",
                                     "libelle": "Faible"
                                 },
                                 {
                                     "code": "medium",
                                     "libelle": "Moyenne"
                                 }
                             ],
                             "skill_level": [
                                 {
                                     "code": "pro",
                                     "libelle": "Professionnel"
                                 },
                                 {
                                     "code": "semipro",
                                     "libelle": "Confirm\u00e9"
                                 },
                                 {
                                     "code": "noexp",
                                     "libelle": "Amateur"
                                 }
                             ],
                             "quality_need": [
                                 {
                                     "code": "max",
                                     "libelle": "Qualit\u00e9 Max"
                                 },
                                 {
                                     "code": "good",
                                     "libelle": "Qualit\u00e9 Bonne"
                                 },
                                 {
                                     "code": "noexp",
                                     "libelle": "Qualit\u00e9 Amateur"
                                 },
                                 {
                                     "code": "na",
                                     "libelle": "Non Applicable"
                                 }
                             ],
                             "contract_type": [
                                 {
                                     "code": "volonteer",
                                     "libelle": "B\u00e9n\u00e9vole"
                                 },
                                 {
                                     "code": "sharedprice",
                                     "libelle": "Montant revers\u00e9"
                                 },
                                 {
                                     "code": "sharedprime",
                                     "libelle": "Part revers\u00e9e"
                                 }
                             ],
                             "transporter_type": [
                                 {
                                     "code": "tran",
                                     "libelle": "Transporter"
                                 }
                             ],
                             "capacity_value": [
                                 {
                                     "code": "truck",
                                     "libelle": "Camionnette"
                                 },
                                 {
                                     "code": "batch30",
                                     "libelle": "30 lots"
                                 }
                             ],
                             "capacity_type": [
                                 {
                                     "code": "class",
                                     "libelle": "class"
                                 },
                                 {
                                     "code": "volume",
                                     "libelle": "volume"
                                 },
                                 {
                                     "code": "units",
                                     "libelle": "units"
                                 }
                             ],
                             "range_type": [
                                 {
                                     "code": "km",
                                     "libelle": "km"
                                 },
                                 {
                                     "code": "dept",
                                     "libelle": "departement"
                                 }
                             ],
                             "provider_type": [
                                 {
                                     "code": "fm",
                                     "libelle": "Fournisseur mat\u00e9riaux"
                                 },
                                 {
                                     "code": "pre",
                                     "libelle": "Pressing"
                                 },
                                 {
                                     "code": "ent",
                                     "libelle": "Entrep\u00f4t"
                                 }
                             ],
                             "provider_subtype": [
                                 {
                                     "code": "fta",
                                     "libelle": "Fournisseur Textile Classe A"
                                 },
                                 {
                                     "code": "ftb",
                                     "libelle": "Fournisseur Textile Classe B"
                                 },
                                 {
                                     "code": "ft3d",
                                     "libelle": "Fournisseur Impression 3D"
                                 }
                             ],
                             "customer_type": [
                                 {
                                     "code": "med",
                                     "libelle": "M\u00e9dical"
                                 },
                                 {
                                     "code": "pres",
                                     "libelle": "Pressing"
                                 },
                                 {
                                     "code": "ent",
                                     "libelle": "Entrep\u00f4t"
                                 },
                                 {
                                     "code": "ins",
                                     "libelle": "Institution"
                                 },
                                 {
                                     "code": "com",
                                     "libelle": "Commerce"
                                 },
                                 {
                                     "code": "gsu",
                                     "libelle": "Grande Surface"
                                 }
                             ],
                             "customer_subtype": [
                                 {
                                     "code": "hop",
                                     "libelle": "Hopital"
                                 },
                                 {
                                     "code": "cli",
                                     "libelle": "Clinique"
                                 },
                                 {
                                     "code": "soilib",
                                     "libelle": "Soignant Lib\u00e9rale"
                                 },
                                 {
                                     "code": "enta",
                                     "libelle": "Entreprise Classe A"
                                 },
                                 {
                                     "code": "entb", "libelle": "Entreprise Classe B"
                                 },
                                 {
                                     "code": "entc", "libelle": "Entreprise Classe C"
                                 }
                             ]
                         })

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
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/organizations/2'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'id': 1000,
                          'vid': 2,
                          'role': 'pro',
                          'status': 'running',
                          'availability': 'midtime',
                          'address': {'street': '30 rue des visiteurs',
                                      'zipcode': '54344',
                                      'city': 'covid-19',
                                      'lon': None, 'lat': None},
                          'data': {'type': 'fm',
                                   'subtype': 'fta'}
                          }
                         )

    def test_update_provider_status(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/organizations/2'
        response = self.put(url, token, {"status": "rejected"})

        self.assertEqual(response.status_code, 204)

        obj = get_organisation(2)
        self.assertEqual(obj.status_obj.code, "rejected")

    def test_search_organizations(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/organizations'
        response = self.get(url, token)
        self.assertEqual(response.status_code, 200)
        self.assertIn("organizations", response.json)
        self.assertEqual(6, len(response.json["organizations"]))

    def test_search_organizations_pagination(self):
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/organizations'
        response = self.get(url, token, {"page": 2, "size": 2})
        self.assertEqual(response.status_code, 200)
        self.assertIn("organizations", response.json)
        self.assertEqual(2, len(response.json["organizations"]))
        self.assertEqual(response.json["organizations"],
                         [{'id': 1002, 'vid': 3, 'role': 'cus', 'status': 'running', 'availability': 'midtime',
                           'address': {'street': '30 rue clients', 'zipcode': '96344', 'city': 'Chanceux', 'lon': None,
                                       'lat': None}, 'data': {'type': 'med', 'subtype': 'hop'}},
                          {'id': 1003, 'vid': 5, 'role': 'cus', 'status': 'active', 'availability': 'fulltime',
                           'address': {'street': '30 rue transporter', 'zipcode': '34344', 'city': 'Sauvequipeut',
                                       'lon': None, 'lat': None},
                           'data': {'type': 'tran', 'capacity': {'type': 'class', 'value': 'class'},
                                    'range': {'type': 'km', 'value': 2}}}]
                         )
