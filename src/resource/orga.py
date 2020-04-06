from flask_jwt_extended import jwt_required
from flask_restful import Resource
from util.validator import parse_params
from flask_restful_swagger import swagger

from serializer.orga import OrganisationSerializer, ReferencesSerializer, OrganisationUpdateSerializer

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
        return ref_repository.get_references(), 200


class OrganisationsApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='Organisation management',
        responseClass=OrganisationSerializer.__name__,
        nickname='organisations',
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
                "message": "Organisation is created."
            }

        ])
    @parse_params(
        {'name': 'vid', 'type': str, 'required': True},
        {'name': 'name', 'type': str, 'required': True},
        {'name': 'role', 'type': str, 'required': True},
        {'name': 'status', 'type': str, 'required': True},
        {'name': 'availability', 'type': str},
        {'name': 'user', 'type': dict, 'required': True},
        {'name': 'address', 'type': dict, 'required': True},
        {'name': 'provider', 'type': dict},
        {'name': 'customer', 'type': dict},
        {'name': 'manufactor', 'type': dict},
        {'name': 'transporter', 'type': dict}
    )
    def post(self, params):
        obj, errors = orga_validator.check_organisation(params)
        if errors:
            return {"errors": errors}, 400
        dbobj = orga_repository.create_organization(obj)
        return dbobj.json, 200


class OrganisationApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='Organisation get',
        responseClass=OrganisationSerializer.__name__,
        nickname='organisation',
        responseMessages=[
            {
                "code": 200,
                "message": "Organisation object."
            }

        ])
    def get(self, vid):
        dbobj = orga_repository.get_organisation(vid)
        if not dbobj:
            return {"errors": [{"code": "UNKNOWN_RESOURCE",
                                "message": "unknown organisation"}]}, 404
        return dbobj.json, 200

    @swagger.operation(
        notes="Update organisation's status",
        nickname='organisation',
        parameters=[
            {
                "name": "body",
                "description": "Organization update parameter",
                "required": True,
                "allowMultiple": False,
                "dataType": OrganisationUpdateSerializer.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 204,
                "message": "Update status succesfully."
            },
            {
                "code": 400,
                "message": "Bad status."
            },
            {
                "code": 404,
                "message": "Unknown ressource."
            }

        ])
    @parse_params(
        {'name': 'status', 'type': str, 'required': True},
    )
    def put(self, vid, params):
        dbobj = orga_repository.get_organisation(vid)
        if not dbobj:
            return {"errors": [{"code": "UNKNOWN_RESOURCE",
                                "message": "unknown organisation"}]}, 404

        statusobj = ref_repository.get_reference_from_code_or_libelle(params.get('status'))
        if not statusobj:
            return {"errors": [{"code": "BAD_STATUS",
                                "message": "bad status"}]}, 400

        dbobj.status_obj = statusobj
        dbobj.save()

        return {}, 204




