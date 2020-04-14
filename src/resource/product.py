import datetime

from flask import request, jsonify, g
import constant

from flask_restful import  Resource
from flask_restful_swagger import swagger

from flask_jwt_extended import create_access_token, jwt_required

from repository import (reference as ref_repository,
                        orga as orga_repository,
                        product as product_repository)
from serializer.product import (ProductListResponseSerializer, ProductSerializer,
                                ProductEquivalenceListRequestSerializer,
                                StockListResponseSerializer, StockCreationRequestSerializer, StockResponseSerializer)

from validator import orga as orga_validator, product as product_validator
from util.validator import parse_params, get_error_messages


class ProductsApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='List of products',
        responseClass=ProductListResponseSerializer.__name__,
        nickname='products',
        parameters=[
            {
                "name": "page",
                "description": "page number",
                "required": True,
                "allowMultiple": False,
                "dataType": "int",
                "paramType": "body"
            },
            {
                "name": "size",
                "description": "number of items returned",
                "required": False,
                "default": 10,
                "allowMultiple": False,
                "dataType": "int",
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "List of products."
            }

        ])
    @parse_params(
        {'name': 'page', 'type': int, "default": 1},
        {'name': 'size', 'type': int, "default": 10},
    )
    def get(self, params):
        obj = product_repository.list_product_references(params.get("page"), params.get("size"))
        return {"products": obj}, 200

    @swagger.operation(
        notes='Product creation',
        responseClass=ProductSerializer.__name__,
        nickname='products',
        parameters=[
            {
                "name": "product_type",
                "description": "type is an enum (material or final)",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "reference",
                "description": "Product reference",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "libelle",
                "description": "Product description",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Product inserted."
            }

        ])
    def post(self):
        params = request.json
        errors = product_validator.ProductCreationRequest().validate(params, many=False)
        if errors:
            return {"errors": [{"code": "BAD_INPUT", "message": "\n".join(errors)}]}, 400

        product_type = params.get("product_type")
        ref = params.get("reference")
        libelle = params.get("libelle")
        product_type = product_repository.ProductType.get_value(product_type)

        obj = product_repository.create_product_reference(product_type, ref, libelle)
        return obj.to_json(), 200


class ProductApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='get products',
        responseClass=ProductSerializer.__name__,
        nickname='product',
        parameters=[
            {
                "name": "reference",
                "description": "Product's reference",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "List of products."
            }

        ])
    def get(self, reference):
        obj = product_repository.get_product_reference_by_reference(reference)
        if obj is None:
            return {"errors":  [get_error_messages(constant.UNKNOWN_RESOURCE)]}, 404
        return obj.to_json(), 200

    @swagger.operation(
        notes='Update products',
        nickname='products',
        responseClass=ProductSerializer.__name__,
        parameters=[
            {
                "name": "reference",
                "description": "Product's reference",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path"
            },
            {
                "name": "materials",
                "description": "List of product equivalence",
                "required": True,
                "allowMultiple": False,
                "dataType": ProductEquivalenceListRequestSerializer.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Product updated."
            }

        ])
    def put(self, reference):

        product = product_repository.get_product_reference_by_reference(reference)
        if product is None:
            return {"errors": [get_error_messages(constant.UNKNOWN_RESOURCE)]}, 404

        params = request.json
        errors = product_validator.ProductEquivalenceList().validate(params, many=False)
        if errors:
            return {"errors": [{"code": "BAD_INPUT", "message": "\n".join(errors)}]}, 400

        errors = []
        if product.type != product_repository.ProductType.final:
            errors.append(get_error_messages(constant.BAD_FINAL_PRODUCT, product.reference))

        materials = params.get("materials")
        for i, mat in enumerate(materials):
            material = product_repository.get_product_reference_by_reference(mat.get("reference"))
            if not material:
                errors.append(get_error_messages(constant.BAD_MATERIAL_PRODUCT, mat.get("reference")))

        if errors:
            return {"errors": errors}, 400

        for mat in materials:
            product_repository.create_equivalence(product, mat.get("reference"), mat.get("count"))

        product.refresh()

        return product.to_json(), 200


class StocksApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='List of stocks',
        responseClass=StockListResponseSerializer.__name__,
        nickname='stocks-list',
        parameters=[
            {
                "name": "page",
                "description": "page number",
                "required": True,
                "allowMultiple": False,
                "dataType": "int",
                "paramType": "body"
            },
            {
                "name": "size",
                "description": "number of items returned",
                "required": False,
                "default": 10,
                "allowMultiple": False,
                "dataType": "int",
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "List of stocks."
            }

        ])
    @parse_params(
        {'name': 'page', 'type': int, "default": 1},
        {'name': 'size', 'type': int, "default": 10},
    )
    def get(self, params):
        obj = product_repository.count_all_stocks_by_reference_and_type(params.get("page"), params.get("size"))

        def clean(it):
            return {
                "reference": it[0],
                "type": product_repository.ProductType.get_name(it[1]),
                "count": it[2]
            }
        return {"total": obj.total,
                "page": params.get("page"),
                "size": params.get("size"),
                "stocks": [clean(it) for it in obj.items]}, 200

    @swagger.operation(
        notes='Stock creation',
        responseClass=StockCreationRequestSerializer.__name__,
        nickname='stocks-creation',
        parameters=[
            {
                "name": "reference",
                "description": "Product reference",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": " count",
                "description": "Product count",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "store inserted inserted."
            },
            {
                "code": 400,
                "message": "params errors."
            },
            {
                "code": 404,
                "message": "unknown product reference."
            }

        ])
    def post(self):
        params = request.json
        errors = product_validator.StockCreationRequest().validate(params, many=False)
        if errors:
            return {"errors": [{"code": "BAD_INPUT", "message": "\n".join(errors)}]}, 400

        product = product_repository.get_product_reference_by_reference(params.get('reference'))
        if product is None:
            return {"errors": [get_error_messages(constant.UNKNOWN_RESOURCE)]}, 404

        prod_type = product_repository.ProductType
        if product.type == prod_type.final:
            # check the material availability
            try:
                product_repository.check_kit_stock_creation(product, params.get("count"))
            except product_repository.ProductException as exc:
                return {"errors": exc.details}, 400

        func = product_repository.create_kit_stock if product.type == prod_type.final \
            else product_repository.create_material_stock
        obj = func(product, params.get("count"))

        return obj.to_json(), 200


class StockApi(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='get a stock count',
        responseClass=StockResponseSerializer.__name__,
        nickname='stocks-get',
        responseMessages=[
            {
                "code": 200,
                "message": "Get a sock."
            }

        ])
    def get(self, reference):
        obj = product_repository.get_stock_by_reference(reference)
        if obj is None:
            return {"errors": [get_error_messages(constant.UNKNOWN_RESOURCE)]}, 404
        return obj, 200



