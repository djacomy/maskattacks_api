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
