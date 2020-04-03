import datetime
import json

from flask import request, jsonify, g
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import  Resource
from flask_restful_swagger import swagger

from serializer.user import (SignupRequestSerializer, SignupResponseSerializer,
                             SigninRequestSerializer, SigninResponseSerializer)

from model.abc import db
from model import User
from util import parse_params


from sqlalchemy.orm.exc import NoResultFound


class SignupApi(Resource):

    @swagger.operation(
        notes='Signup',
        responseClass=SignupResponseSerializer.__name__,
        nickname='signup',
        parameters=[
            {
                "name": "body",
                "description": "signup's parameter",
                "required": True,
                "allowMultiple": False,
                "dataType": SignupRequestSerializer.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "User is created."
            }

        ])
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.set_password(body.get("password"))
        user.save()
        id = user.id
        return {'id': str(id)}, 200


class LoginApi(Resource):

    @swagger.operation(
        notes='Signin',
        responseClass=SigninResponseSerializer.__name__,
        nickname='signup',
        parameters=[
            {
                "name": "body",
                "description": "signin's parameter",
                "required": True,
                "allowMultiple": False,
                "dataType": SigninRequestSerializer.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "A session token is provider."
            },
            {
                "code": 404,
                "message": "Email not found"
            },
            {
                "code": 401,
                "message": "Password invalid"
            }


        ])
    def post(self):
        body = request.get_json()
        user = User.query.filter_by(email=body.get('email')).first()
        if not user:
            return {"error": "Email not found"}, 404

        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Password invalid'}, 401

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
        return user.json, 200

    def put(self, id):
        body = request.get_json()
        user = User.query.get(id)

        for k, v in body.items():
            if v == getattr(user, k):
                continue
            setattr(user, k, v)
        user.save()
        return user.json, 200

    def delete(self, id):
        try:
            user = User.query.get(id)
            user.remove()
            return {}, 204

        except NoResultFound:
           response = jsonify(data={"errors": [{"user": "Not found"}]})
           response.status_code = 404
           return response



