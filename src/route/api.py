import os
from flask import Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger

from config import BASE_SERVER_PATH
from resource.user import SignupApi, LoginApi
from resource.orga import OrganisationsApi, OrganisationApi
from resource.product import RequestApi, KitsApi, KitApi, ProtectionsApi, ProtectionApi, BatchesApi, BatchApi
from resource.stock import StocksApi, StockApi
from resource.user import UserAPI, UserListAPI

api_blueprint = Blueprint('api', __name__)

api = swagger.docs(Api(api_blueprint), apiVersion='0.1',
                   basePath=BASE_SERVER_PATH,
                   resourcePath='/',
                   produces=["application/json", "text/html"],
                   api_spec_url='/docs',
                   description='Mask attacks api')

api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')

api.add_resource(OrganisationsApi, '/organizations')
api.add_resource(OrganisationApi, '/organization/<int:vid>')

api.add_resource(RequestApi, '/requests')

api.add_resource(KitsApi, '/kits')
api.add_resource(KitApi, '/kits/<int:id>')

api.add_resource(ProtectionsApi, '/protections')
api.add_resource(ProtectionApi, '/protections/<int:id>')

api.add_resource(BatchesApi, '/batches')
api.add_resource(BatchApi, '/batches/<int:id>')


api.add_resource(StocksApi, '/stocks')
api.add_resource(StockApi, '/stocks/<int:id>')


api.add_resource(UserListAPI, '/users')
api.add_resource(UserAPI, '/users/<int:id>')

