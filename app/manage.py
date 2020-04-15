from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from commands.fixture import DumpCommand, ImportReferenceCommand, LoadFixturesCommand


import config
from maskattacks.model.abc import db
from app import create_app

app = create_app(config)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('dump', DumpCommand)
manager.add_command('import_ref', ImportReferenceCommand)
manager.add_command('load_fixtures', LoadFixturesCommand)

if __name__ == '__main__':
    manager.run()
