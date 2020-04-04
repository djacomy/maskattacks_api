from flask_jwt_extended import jwt_required
from flask_restful import Resource
from util.validator import parse_params
from flask_restful_swagger import swagger

from serializer.orga import OrganisationSerializer, ReferencesSerializer

from repository import reference as ref_repository, orga as orga_repository
from validator import orga as orga_validator



class ReferencesApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='List of value available of organisation field',
        responseClass=ReferencesSerializer.__name__,
        nickname='references',
        responseMessages=[
            {
                "code": 200,
                "message": "List of references data, need to create an organisation "
            }

        ])
    def get(self):
        return ref_repository.get_reference_codes(), 200


class OrganisationApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='Organisation management',
        responseClass=OrganisationSerializer.__name__,
        nickname='organisation',
        parameters=[
            {
                "name": "body",
                "description": "Organization parameter",
                "required": True,
                "allowMultiple": False,
                "dataType": OrganisationSerializer.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "User is created."
            }

        ])
    @parse_params(
        {'name': 'name', 'type': str, 'required': True},
        {'name': 'role', 'type': str, 'required': True},
        {'name': 'status', 'type': str, 'required': True},
        {'name': 'availability', 'type': str},
        {'name': 'address', 'type': dict},
        {'name': 'provider', 'type': dict},
        {'name': 'customer', 'type': dict},
        {'name': 'manufactor', 'type': dict},
        {'name': 'transporter', 'type': dict}
    )
    def post(self, params):
        obj, errors = orga_validator.check_organisation(params)

        for field in {"address": orga_validator.check_address,
                      "provider": orga_validator.check_provider,
                      "customer": orga_validator.check_customer,
                      "manufactor": orga_validator.check_manufactor,
                      "transporter": orga_validator.check_transporter}.items():
            if params.get(field) is None:
                continue

            nested_obj, nested_errors = orga_validator.check_address(params.get("address"))
            obj[field] = nested_obj
            errors += nested_errors

        if errors:
            return {"errors": errors}, 400

        return obj, 200

