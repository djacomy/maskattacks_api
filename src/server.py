from flask import Flask
from flask.ext.cors import CORS
from flask_jwt_extended import JWTManager

import config
from model.abc import db

server = Flask(__name__)
server.debug = config.DEBUG

server.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
server.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db.init_app(server)
jwt = JWTManager(server)
db.app = server


CORS(
    server,
    resources={r"/*": {"origins": "*"}},
    headers=['Content-Type', 'X-Requested-With', 'Authorization']
)
from route.api import api_blueprint
server.register_blueprint(api_blueprint, url_prefix="/api")

from route.common import common_blueprint
server.register_blueprint(common_blueprint, url_prefix="/")


if __name__ == '__main__':
    server.run(host=config.HOST, port=config.PORT)
