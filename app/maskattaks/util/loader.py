import csv
import os
import importlib

from config import DATA_DIR
from maskattaks.model.orga import ReferenceType, Reference


def dump_fixtures(model):
    res = []
    module_name, class_name = model.rsplit('.', 1)
    module = importlib.import_module(module_name)
    l_model = getattr(module, class_name)
    for item in l_model.query.all():
        res.append(item.json)
    return [{
        "model": model,
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
