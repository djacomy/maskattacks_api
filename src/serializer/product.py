from flask_restful_swagger import swagger
from flask_restful import fields


class ProductEquivalenceSerializer:
    resource_fields = {
        'id': fields.Integer,
        'reference': fields.String,
        'type': fields.String,
        'count': fields.String()
    }
    required = ['id', "reference"]


@swagger.model
@swagger.nested(organizations=ProductEquivalenceSerializer.__name__)
class ProductSerializer:
    resource_fields = {
        'id': fields.Integer,
        'reference': fields.String,
        'type': fields.String,
        'materials': fields.Nested(ProductEquivalenceSerializer.resource_fields)
    }
    required = ['id', "reference", 'type']


@swagger.model
@swagger.nested(products=ProductSerializer.__name__)
class ProductListResponseSerializer:
    resource_fields = {
        'products': fields.List(fields.Nested(ProductSerializer.resource_fields)),
    }


@swagger.model
class ProductEquivalenceRequesterializer:
    resource_fields = {
        'reference': fields.String,
        'count': fields.Integer
    }
    required = ["reference", "count"]


@swagger.model
@swagger.nested(materials=ProductEquivalenceRequesterializer.__name__)
class ProductEquivalenceListRequestSerializer:
    resource_fields = {
        'materials': fields.List(fields.Nested(ProductEquivalenceRequesterializer.resource_fields)),
    }



