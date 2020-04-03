from flask_migrate import Migrate, MigrateCommand
from flask_script import Command, Manager, Server, Shell
from commands.fixture import DumpCommand, ImportReferenceCommand


import config
from model.abc import db
from app import create_app

app = create_app(config)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('dump', DumpCommand)
manager.add_command('import_ref', ImportReferenceCommand)

if __name__ == '__main__':
    manager.run()
