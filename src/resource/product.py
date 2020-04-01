import datetime

from flask import request, jsonify, g

from flask_restful import  Resource
from flask_restful_swagger import swagger

from flask_jwt_extended import create_access_token, jwt_required

from model.abc import db
from model import User
from util import parse_params


from sqlalchemy.orm.exc import NoResultFound

protection_types = ["mask_efp2", "mask_chirurg", "mask_toile"]

request_list = [{"id": 1, "institution": "Hopital de Quimper", 'product_type': "mask_efp2", "count": "25", "pro": True,
                 "create_timestamp": "2020-03-20T20:00:00", "status": "submitted"},
                {"id": 2, "institution": "Hopital de Quimper", 'product_type': "mask_toile", "count": "43", "pro": True,
                 "create_timestamp": "2020-03-20T20:00:00", "status": "submitted"}
                ]

product_list = [{"id": 1, "request_id": 1,  "product_type": "kit", 'origin': "entrepot1",
                 "destination": "couturier1", "status": "to_build"},
                {"id": 2, "request_id": 1, "reference": "XXXX234",  "product_type": "mask_efp2", 'origin': "couturier1",
                 "destination": "entrepot1", "status": "wait"},
                {"id": 3, "request_id": 1, "reference": "XXXX234", "product_type": "mask_efp2", 'origin': "entrepot1",
                 "destination": "Hopital de Quimper", "status": "wait"},
                {"id": 4, "request_id": 1, "reference": "XXXX236", "product_type": "mask_toile", 'origin': "entrepot1",
                "destination": "Hopital de Quimper", "status": "deliver"}

                ]

batch_list = []


class RequestApi(Resource):
    method_decorators = [jwt_required]

    def get(self):
        return {'requests': request_list}, 200

    def post(self):
        body = request.get_json()
        errors = []

        for f in ["institution", "product_type", "count", "pro"]:
            if body.get(f) is None:
                errors.append(f"{f} is required")
            elif f == "product_type" and body.get(f) not in protection_types:
                errors.append(f"{f} requires value belonged {','.join(protection_types)}")
            elif f == "pro":
                try:
                    bool(body.get(f))
                except:
                    errors.append(f"{f} is a boolean")

        if errors:
            return {"errors": errors}, 400

        body["id"] = len(request_list)
        body["create_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%i")
        body["status"] = "submitted"
        body["pro"] = True

        # define logistic items.
        index = len(product_list)
        product_list.append({
            "id": index+1,
            "request_id": body["id"],
            "product_type": "kit",
            'origin': "entrepot1",
            "destination": "couturier1",
            "status": "to_build"
        })

        product_list.append({
            "id": index + 2,
            "request_id": body["id"],
            "product_type": body["product_type"],
            'origin': "couturier1",
            "destination": "entrepot1" if body["pro"] else body["institution"],
            "status": "to_build"
        })

        if body["pro"]:
            product_list.append({
                "id": index + 3,
                "request_id": body["id"],
                "product_type": body["product_type"],
                'origin': "entrepot1",
                "destination": body["institution"],
                "status": "to_build"
            })
        request_list.append(body)
        return body, 200


class KitsApi(Resource):
    method_decorators = [jwt_required]

    def get(self):
        return {'kits': [p for p in product_list if p["product_type"] == "kit"]}, 200


class KitApi(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        obj = [item for item in product_list if item["id"] == id]
        if not obj:
            return {"errors": "Not found"}, 404

        if obj[0]["product_type"] != "kit":
            return {"errors": "Not a kit"}, 404

        return obj, 200

    def put(self, id):
        body = request.get_json()

        obj = [item for item in product_list if item["id"] == id]
        if not obj:
            return {"errors": "Not found"}, 404

        if obj[0]["product_type"] != "kit":
            return {"errors": "Not a kit"}, 404

        for field in ["status", "assignee"]:
            if body.get("status") is not None and body.get(field) != obj[0].get(field):
                obj[0][field] = body.get(field)

        return obj[0], 200


class ProtectionsApi(Resource):
    method_decorators = [jwt_required]

    def get(self):
        return {'kits': [p for p in product_list if p["product_type"] != "kit"]}, 200


class ProtectionApi(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        obj = [item for item in product_list if item["id"] == id]
        if not obj:
            return {"errors": "Not found"}, 404

        if obj[0]["product_type"] == "kit":
            return {"errors": "Not a product"}, 404

        return obj, 200

    def put(self, id):
        body = request.get_json()
        obj = [item for item in product_list if item["id"] == id]
        if not obj:
            return {"errors": "Not found"}, 404

        if obj[0]["product_type"] == "kit":
            return {"errors": "Not a procuct"}, 404

        for field in ["status", "assignee"]:
            if body.get("status") is not None and body.get(field) != obj[0].get(field):
                obj[0][field] = body.get(field)

        return obj[0], 200


class BatchesApi(Resource):
    method_decorators = [jwt_required]

    def get(self):
        return {"batches": batch_list}, 200

    def post(self):
        body = request.get_json()

        products = [p for p in product_list if p["id"] in body.get("products")]
        if not products:
            return {"error": "No products found"}, 400

        destination = {p["destination"] for p in products}
        if len(destination) != 1:
            return {"error": "Not the same destination"}, 400
        batch = {
            "id": len(batch_list),
            "create_timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%i"),
            "destination": list(destination)[0],
            "status": "submitted"
        }
        batch_list.append(batch)

        return batch, 200


class BatchApi(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        batch = [b for b in batch_list if b["id"]== id]
        if not batch:
            return {"error": "No batch found"}, 404

        return batch[0], 200

    def put(self, id):
        body = request.get_json()

        batch = [b for b in batch_list if b["id"] == id]
        if not batch:
            return {"error": "No batch found"}, 404

        for field in ["status", "assignee"]:
            if body.get("status") is not None and body.get(field) != batch[0].get(field):
                batch[0][field] = body.get(field)
        return batch[0], 200


