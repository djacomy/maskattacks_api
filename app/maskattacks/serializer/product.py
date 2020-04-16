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


@swagger.model
class StockResponseSerializer:
    resource_fields = {
        'reference': fields.String,
        'type': fields.String,
        'count': fields.Integer
    }
    required = ["reference", "count"]


@swagger.model
@swagger.nested(stocks=StockResponseSerializer.__name__)
class StockListResponseSerializer:
    resource_fields = {
        'total': fields.Integer,
        'page': fields.Integer,
        'size': fields.Integer,
        'stocks': fields.List(fields.Nested(StockResponseSerializer.resource_fields)),

    }

@swagger.model
class StockCreationRequestSerializer:
    resource_fields = {
        'type': fields.String,
        'reference': fields.String,
        'count': fields.Integer
    }
    required = ['type', "reference", 'count']


@swagger.model
class DeliveryItemResponseSerializer:
    resource_fields = {
        'reference': fields.String,
        'manufactor': fields.String,
        'type': fields.String,
        'count': fields.Integer
    }
    required = ["reference", "manufactor", "type", "count"]


@swagger.model
@swagger.nested(results=DeliveryItemResponseSerializer.__name__)
class DeliveryItemListResponseSerializer:
    resource_fields = {
        'total': fields.Integer,
        'page': fields.Integer,
        'size': fields.Integer,
        'results': fields.List(fields.Nested(DeliveryItemResponseSerializer.resource_fields)),
    }
    required = ["total", "page", "size", "results"]


@swagger.model
class DeliveryItemUnitSerializer:
    resource_fields = {
        'type': fields.String,
        'manufactor': fields.String,
        'count': fields.Integer
    }
    required = ["type", "manufactor", "count"]


@swagger.model
@swagger.nested(deliveries=DeliveryItemUnitSerializer.__name__)
class DeliveryItemRefResponseSerializer:
    resource_fields = {
        'reference': fields.String,
        'deliveries': fields.List(fields.Nested(DeliveryItemUnitSerializer.resource_fields)),

    }
    required = ["reference", "deliveries"]

    @swagger.model
    class DeliveryItemResponseSerializer:
        resource_fields = {
            'reference': fields.String,
            'manufactor': fields.String,
            'type': fields.String,
            'count': fields.Integer
        }
        required = ["reference", "count"]



@swagger.model
class BatchResponseSerializer:
    resource_fields = {
        'reference': fields.String,
        'status': fields.String,
        'product_reference': fields.String,
        'delivery_type': fields.String,
        'destination': fields.String,
        'transporter': fields.String,
        'type': fields.String,
        'count': fields.Integer
    }
    required = ["reference", "status", "product_reference",  "delivery_type", "count"]


@swagger.model
@swagger.nested(results=BatchResponseSerializer.__name__)
class BatchListResponseSerializer:
    resource_fields = {
        'total': fields.Integer,
        'page': fields.Integer,
        'size': fields.Integer,
        'results': fields.List(fields.Nested(BatchResponseSerializer.resource_fields)),
    }
    required = ["total", "page", "size", "results"]
