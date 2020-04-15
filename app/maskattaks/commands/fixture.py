import json
import os

from flask import current_app
from flask_script import Command
from flask_fixtures import load_fixtures, loaders

from maskattaks.model import db
from maskattaks.util.loader import import_references, dump_fixtures


class ImportReferenceCommand(Command):
    """Class ImpportReferencesCommand."""

    description = "Import reference Command"

    option_list = (
    )

    def run(self):
        import_references()


class DumpCommand(Command):
    """Class DumpCommand."""

    description = "Dump modele command"

    option_list = (
    )

    def run(self):
        with open("dump.json", "w") as fp:
            json.dump(dump_fixtures(), fp)


class LoadFixturesCommand(Command):

    def run(self):

        db.drop_all()
        # Setup the database
        db.create_all()
        # Rollback any lingering transactions
        db.session.rollback()

        # Construct a list of paths within which fixtures may reside
        default_fixtures_dir = os.path.join(current_app.root_path, 'fixtures')
        # All relative paths should be relative to the app's root directory.
        fixtures_dirs = [default_fixtures_dir]

        # Load all of the fixtures
        for filename in ["refs.json", "orga.json", "product.json"]:
            for directory in fixtures_dirs:
                filepath = os.path.join(directory, filename)
                if not os.path.exists(filepath):
                    continue

                load_fixtures(db, loaders.load(filepath))
                break

            else:
                raise IOError("Error loading '{0}'. File could not be found".format(filename))
