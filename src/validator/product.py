from marshmallow import Schema, fields


class ProductEquivalenceRequest(Schema):
    reference = fields.String()
    count = fields.Integer()


class ProductEquivalenceList(Schema):
    materials = fields.Nested(ProductEquivalenceRequest, many=True)
