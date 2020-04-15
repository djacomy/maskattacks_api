from copy import deepcopy
from maskattacks.model.user import *
from maskattacks.model.orga import *

"""
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
"""

def _creat_obj(field, params):
    """

    :param field
    :param params:
    :return:
    """
    model = {
        "user": User,
        "address": Address,
        "provider": Provider,
        "transporter": Transporter,
        "customer": Customer,
        "manufactor": Manufacturor,
    }
    item = model.get(field)(**params)
    item.save()
    return item


def create_organization(params):
    tmp = deepcopy(params)
    objs = {}
    for field in ['user', 'address', "provider", "transporter", "customer", "manufactor"]:
        nested_data = tmp.pop(field, None)
        if nested_data is None:
            continue
        obj = _creat_obj(field, nested_data)
        objs[field] = obj

    orga = Organisation(**tmp)
    for field in ['user', 'address', "provider", "transporter", "customer", "manufactor"]:
        item = objs.pop(field, None)
        if item is None:
            continue
        if hasattr(orga, field):
            setattr(orga, field, item)
        else:
            setattr(orga, "data", item)

    orga.save()
    return orga


def get_organisations(page=1, pernumber=10):
    return [item.json for item in Organisation.query.paginate(page, per_page=pernumber).items]

def get_organisation(vid):
    return Organisation.query.filter(Organisation.vid == vid).first()


def get_provider(id):
    return Provider.query.filter(Provider.id == id)
