from flask_restful_swagger import swagger
from flask_restful import fields


@swagger.model
class ReferenceSerializer:
    resource_fields = {
        'code': fields.String,
        'libelle': fields.String,
    }


@swagger.model
@swagger.nested(references=ReferenceSerializer.__name__)
class ReferencesSerializer:
    resource_fields = {
        'references': fields.List(fields.Nested(ReferenceSerializer.resource_fields))
    }


@swagger.model
class AddressSerializer:
    resource_fields = {
        'street': fields.String,
        'zipcode': fields.String,
        'city': fields.String,
        'lon': fields.Float,
        'lat': fields.Float
    }
    required = ["street", "zipcode", 'city']


@swagger.model
class ManufactorSerializer:
    resource_fields = {
        'type': fields.String,
        'capacity': fields.String,
        'skill_level': fields.String,
        'quality_need': fields.String,
        'contract_type': fields.String,
    }
    required = ["street", "zipcode", 'city']


@swagger.model
class CapacitySerializer:
    resource_fields = {
        'type': fields.String,
        'value': fields.Integer,
    }
    required = ["type", "value"]


@swagger.model
class RangeSerializer:
    resource_fields = {
        'type': fields.String,
        'value': fields.String,
    }
    required = ["type", "value"]


@swagger.model
@swagger.nested(range=RangeSerializer.__name__)
@swagger.nested(capacity=CapacitySerializer.__name__)
class TransporterSerializer:
    resource_fields = {
        'type': fields.String,
        'capacity': fields.Nested(AddressSerializer.resource_fields),
        'range': fields.Nested(RangeSerializer.resource_fields)
    }
    required = ["type", "range", "capacity"]


class OtherSerializer:
    resource_fields = {
        'type': fields.String,
        'subtype': fields.String
    }
    required = ["type", "subtype"]


@swagger.model
@swagger.nested(stocks=AddressSerializer.__name__)
@swagger.nested(provider=OtherSerializer.__name__)
@swagger.nested(customer=OtherSerializer.__name__)
@swagger.nested(transporter=TransporterSerializer.__name__)
@swagger.nested(manufactor=ManufactorSerializer.__name__)
class OrganisationSerializer:
    resource_fields = {
        'vid': fields.Integer,
        'name': fields.String,
        'role': fields.String,
        'status': fields.String,
        'availability': fields.String,
        'address': fields.Nested(AddressSerializer.resource_fields),
        'provider': fields.Nested(OtherSerializer.resource_fields),
        'customer': fields.Nested(OtherSerializer.resource_fields),
        'transporter': fields.Nested(TransporterSerializer.resource_fields),
        'manufactor': fields.Nested(ManufactorSerializer.resource_fields),
    }
    required = ["name", 'role']

@swagger.model
class UserSerializer:
    resource_fields = {
        "email":fields.String,
        "firstname" :fields.String,
        "lastname": fields.String,
        "password": fields.String,
    }
    required = ["email", "firstname", "lastname", "password"]


@swagger.model
@swagger.nested(user=UserSerializer.__name__)
@swagger.nested(stocks=AddressSerializer.__name__)
@swagger.nested(provider=OtherSerializer.__name__)
@swagger.nested(customer=OtherSerializer.__name__)
@swagger.nested(transporter=TransporterSerializer.__name__)
@swagger.nested(manufactor=ManufactorSerializer.__name__)
class OrganisationResponseSerializer:
    resource_fields = {
        'id': fields.Integer,
        'vid': fields.Integer,
        'name': fields.String,
        'role': fields.String,
        'status': fields.String,
        'availability': fields.String,
        'user': fields.Nested(UserSerializer.resource_fields, allow_null=False),
        'address': fields.Nested(AddressSerializer.resource_fields, allow_null=False),
        'provider': fields.Nested(OtherSerializer.resource_fields),
        'customer': fields.Nested(OtherSerializer.resource_fields),
        'transporter': fields.Nested(TransporterSerializer.resource_fields),
        'manufactor': fields.Nested(ManufactorSerializer.resource_fields),
    }
    required = ["name", 'role', 'status']

