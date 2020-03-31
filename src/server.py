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

from route.common import common_blueprint
server.register_blueprint(common_blueprint, url_prefix="/api/routes")

from route.auth import auth_blueprint
server.register_blueprint(auth_blueprint, url_prefix="/api/auth")

from route.user import user_blueprint
server.register_blueprint(user_blueprint, url_prefix="/api/users")

from route.product import product_blueprint
server.register_blueprint(product_blueprint, url_prefix="/api")

from route.stock import stock_blueprint
server.register_blueprint(stock_blueprint, url_prefix="/api/stocks")


if __name__ == '__main__':
    server.run(host=config.HOST, port=config.PORT)
