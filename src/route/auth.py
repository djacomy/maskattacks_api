from flask import Blueprint
from flask.ext.restful import Api


auth_blueprint = Blueprint('auth', __name__)
auth_blueprint_api = Api(auth_blueprint)


from resource.user import SignupApi, LoginApi

auth_blueprint_api.add_resource(SignupApi, '/signup')
auth_blueprint_api.add_resource(LoginApi, '/login')


