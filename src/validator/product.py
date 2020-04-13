from marshmallow import Schema, fields


class ProductEquivalenceRequest(Schema):
    reference = fields.String(required=True)
    count = fields.Integer(required=True)


class ProductEquivalenceList(Schema):
    materials = fields.Nested(ProductEquivalenceRequest, many=True, required=True)
