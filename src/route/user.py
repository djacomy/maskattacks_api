from flask import Blueprint
from flask.ext.restful import Api


user_blueprint = Blueprint('user', __name__)
user_blueprint_api = Api(user_blueprint)


from resource.user import UserAPI, UserListAPI, SignupApi, LoginApi

user_blueprint_api.add_resource(SignupApi, '/api/auth/signup')
user_blueprint_api.add_resource(LoginApi, '/api/auth/login')

user_blueprint_api.add_resource(UserListAPI, '/api/user')
user_blueprint_api.add_resource(UserAPI, '/api/user/<int:id>')

