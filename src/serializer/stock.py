from flask_restful_swagger import  swagger
from flask_restful import fields


@swagger.model
class StockSerializer:
    resource_fields = {
        'id': fields.Integer,
        'provider': fields.String,
        'kit_type': fields.String,
        'count': fields.Integer
    }


@swagger.model
@swagger.nested(
   stocks=StockSerializer.__name__)
class StockListSerializer:
  resource_fields = {
      'stocks': fields.List(fields.Nested(StockSerializer.resource_fields)),
  }

