import datetime

from flask import request, jsonify, g
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import  Resource
from flask_restful_swagger import swagger

from model.abc import db
from model import User
from util import parse_params


from sqlalchemy.orm.exc import NoResultFound


class SignupApi(Resource):

    def post(self):
        body = request.get_json()
        user = User(**body)
        user.set_password(body.get("password"))
        user.save()
        id = user.id
        return {'id': str(id)}, 200


class LoginApi(Resource):

    def post(self):
        body = request.get_json()
        user = User.query.filter_by(email=body.get('email')).first()
        if not user:
            return {"error": "not found"}, 404

        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200


class UserListAPI(Resource):

    @jwt_required
    def get(self):
        return jsonify(data=[user.json for user in User.query])


class UserAPI(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        user = User.query.get(id)
        user_dict = user.json()
        return user_dict

    def put(self, id):
        body = request.get_json()
        user = User.query.get(id)

        for k, v in body.items():
            if v == getattr(user, k):
                continue
            setattr(user, k, v)
        user.save()
        return user.json()

    def delete(self, id):
        try:
            user = User.query.get(id)
            user.remove()
            return {}, 204

        except NoResultFound:
           response = jsonify(data={"errors": [{"user": "Not found"}]})
           response.status_code = 404
           return response



