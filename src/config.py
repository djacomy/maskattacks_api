import os, logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")

DEBUG = os.getenv("ENVIRONEMENT") == "DEV"
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss')
BASE_SERVER_PATH = os.environ.get("BASE_SERVER_PATH", 'http://192.168.64.3:5000/')

DB_CONTAINER = os.getenv("DB_CONTAINER", "db")

POSTGRES = {
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'pw': os.getenv('POSTGRES_PW', 'postgres'),
    'host': os.getenv('POSTGRES_HOST', DB_CONTAINER),
    'port': os.getenv('POSTGRES_PORT', 5432),
    'db': os.getenv('POSTGRES_DB', 'postgres'),
}
DB_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)


