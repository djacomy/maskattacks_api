from collections import defaultdict

from sqlalchemy import or_

from maskattacks.model.orga import Reference, ReferenceType, Organisation


def find_reference_by_type_and_libelle( type, libelle):
    return Reference.query.filter_by(type=type, libelle=libelle).first()


def find_reference_by_type_and_code(type, code):
    return Reference.query.filter_by(type=type, code=code).first()


def get_roles():
    return {item.id: item.code for item in
            Reference.query.filter(Reference.type == ReferenceType.orga_role).all()}


def get_references():
    result = defaultdict(list)
    for item in Reference.query.all():
        result[ReferenceType.get_name(item.type)].append({
            "code": item.code,
            "libelle": item.libelle})
    return result


def get_reference_codes():
    result = defaultdict(list)
    for item in Reference.query.all():
        result[ReferenceType.get_name(item.type)].append(item.code)
    return result


def get_reference_from_code_or_libelle(value):
    return Reference.query.filter(or_(Reference.code == value, Reference.libelle == value)).first()
