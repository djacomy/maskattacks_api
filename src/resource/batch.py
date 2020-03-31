import datetime

from flask import request, jsonify, g
from flask.ext.restful import Resource
from flask_jwt_extended import create_access_token, jwt_required

from model.abc import db
from model import User
from util import parse_params


from sqlalchemy.orm.exc import NoResultFound

stocks_list = [{"id": 1, "provider": "toto", 'kit_type': "kit1", "count": 10}]


class BatchesApi(Resource):
    method_decorators = [jwt_required]

    def get(self):
        return {'stocks': stocks_list}, 200

    def post(self):
        body = request.get_json()
        stocks_list.append(body)
        return stocks_list, 200


class BatchApi(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        obj = [item for item in stocks_list if item["id"] == id]
        if not obj:
            return {"errors": "Not found"}, 404
        return obj, 200

    def put(self, id):
        body = request.get_json()
        count = body.get("count")
        obj = [item for item in stocks_list if item["id"] == id]
        if not obj:
            return {"errors": "Not found"}, 404

        obj[0]["count"] = count
        return obj[0], 200
