import json
from flask_script import Command

from util.loader import import_references, dump_fixtures


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
