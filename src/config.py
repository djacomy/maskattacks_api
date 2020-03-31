import os, logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss')

POSTGRES = {
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'pw': os.getenv('POSTGRES_PW', 'postgres'),
    'host': os.getenv('POSTGRES_HOST', os.getenv('DB_PORT_5432_TCP_ADDR')),
    'port': os.getenv('POSTGRES_PORT', os.getenv('DB_PORT_5432_TCP_PORT')),
    'db': os.getenv('POSTGRES_DB', 'postgres'),
}
DB_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)


