from flask import Blueprint
from flask.ext.restful import Api


stock_blueprint = Blueprint('stock', __name__)
stock_blueprint_api = Api(stock_blueprint)


from resource.stock import StocksApi, StockApi

stock_blueprint_api.add_resource(StocksApi, '/')
stock_blueprint_api.add_resource(StockApi, '/<int:id>')


