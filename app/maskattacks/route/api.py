import os
from flask import Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger

from config import BASE_SERVER_PATH
from maskattacks.resource.user import SignupApi, LoginApi
from maskattacks.resource.orga import OrganisationsApi, OrganisationApi, ReferencesApi
from maskattacks.resource.user import UserAPI, UserListAPI
from maskattacks.resource.product import (ProductsApi, ProductApi, StocksApi, StockApi,
                                          DeliveryItemsApi, DeliveryItemApi, BatchesApi, BatchApi)

api_blueprint = Blueprint('api', __name__)

api = swagger.docs(Api(api_blueprint), apiVersion='0.1',
                   basePath=BASE_SERVER_PATH,
                   resourcePath='/',
                   produces=["application/json", "text/html"],
                   api_spec_url='/docs',
                   description='Mask attacks api')

api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')

api.add_resource(ReferencesApi, '/references')
api.add_resource(OrganisationsApi, '/organizations')
api.add_resource(OrganisationApi, '/organizations/<int:vid>')

api.add_resource(ProductsApi, '/products')
api.add_resource(ProductApi, '/products/<string:reference>')

api.add_resource(StocksApi, '/stocks')
api.add_resource(StockApi, '/stocks/<string:reference>')

api.add_resource(DeliveryItemsApi, '/deliveryitems')
api.add_resource(DeliveryItemApi, '/deliveryitems/<string:reference>')

api.add_resource(BatchesApi, '/batches')
api.add_resource(BatchApi, '/batches/<string:reference>')

api.add_resource(UserListAPI, '/users')
api.add_resource(UserAPI, '/users/<int:id>')

