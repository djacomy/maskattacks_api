from marshmallow import Schema, fields, validate


class ProductCreationRequest(Schema):
    product_type = fields.String(required=True, validate=validate.OneOf(["materials", "final"]))
    reference = fields.String(required=True)
    libelle = fields.String(required=True)


class PaginationQueryRequest(Schema):
    page = fields.String( default=1)
    size = fields.Integer(default=10)


class ProductEquivalenceRequest(Schema):
    reference = fields.String(required=True)
    count = fields.Integer(required=True)


class ProductEquivalenceList(Schema):
    materials = fields.Nested(ProductEquivalenceRequest, many=True, required=True)


class StockCreationRequest(Schema):
    reference = fields.String(required=True)
    count = fields.Integer(required=True)


class DeliveryItemCreationRequest(Schema):
    reference = fields.String(required=True)
    manufactor_vid = fields.Integer(required=True)
    delivery_type = fields.String(required=True,  validate=validate.OneOf(["kit", "final"]), default="kit")
    count = fields.Integer(required=True)


class BatchCreationRequest(Schema):
    reference = fields.String(required=True)
    delivery_type = fields.String(required=True,  validate=validate.OneOf(["kit", "final"]), default="kit")
    batch_size = fields.Integer(required=True)
