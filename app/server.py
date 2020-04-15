import config
from app import create_app

server = create_app(config)

if __name__ == '__main__':
    server.run(host=config.HOST, port=config.PORT)
