from flask import Blueprint
from flask.ext.restful import Api


product_blueprint = Blueprint('product', __name__)
product_blueprint_api = Api(product_blueprint)


from resource.product import RequestApi, KitsApi, KitApi, ProtectionsApi, ProtectionApi, BatchesApi, BatchApi

product_blueprint_api.add_resource(RequestApi, '/requests')

product_blueprint_api.add_resource(KitsApi, '/kits')
product_blueprint_api.add_resource(KitApi, '/kits/<int:id>')

product_blueprint_api.add_resource(ProtectionsApi, '/protections')
product_blueprint_api.add_resource(ProtectionApi, '/protections/<int:id>')

product_blueprint_api.add_resource(BatchesApi, '/batches')
product_blueprint_api.add_resource(BatchApi, '/batches/<int:id>')
