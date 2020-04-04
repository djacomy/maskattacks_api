from test.utils.mixins import BaseTest, BaseAuthMixin


class TestAuth(BaseTest, BaseAuthMixin):
    fixtures = ["users.json", "refs.json"]

    def test_routes(self):
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
        token = self.authenticate('joe@example.fr', 'super-secret-password')
        url = 'api/organization'
        response = self.post(url, token, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1})

