import csv
import os

from config import DATA_DIR
from model.orga import ReferenceType, Reference


def dump_fixtures():
    res = []
    for item in Reference.query.all():
        res.append(item.json)
    return [{
        "table": Reference.__tablename__,
        "records": res,
    }]


def import_references():
    with open(os.path.join(DATA_DIR, "references.csv"), encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=',')

        for i, row in enumerate(reader):
            if i == 0:
                continue

            obj = Reference(type=ReferenceType.get_value(row[0]),
                            code=row[1], libelle=row[2])
            obj.save()
