import enum
from collections import defaultdict

from sqlalchemy_utils import ChoiceType, generic_relationship


from .abc import db, BaseModel


class Variable(db.Model, BaseModel):
    __tablename__ = 'orga_variable'
    code = db.Column(db.String(10), primary_key=True)
    value = db.Column(db.String(15))


class ReferenceType(enum.Enum):
    manufactor_type = 1
    manufactor_capacity = 2
    skill_level = 3
    quality_need = 4
    contract_type = 5
    transporter_type = 6
    capacity_value = 7
    capacity_type = 8
    range_type = 9
    provider_type = 10
    provider_subtype = 11
    customer_type = 12
    customer_subtype = 13
    orga_status = 14
    orga_availability = 15
    orga_role = 16

    @classmethod
    def get_value(cls, name):
        return getattr(cls, name).value

    @classmethod
    def get_name(cls, value):
        return cls(value).name

    def __int__(self):
        return self.value


class Reference(db.Model, BaseModel):
    __tablename__ = 'orga_reference'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15))
    type = db.Column(ChoiceType(ReferenceType, impl=db.Integer()))
    libelle = db.Column(db.String(30))

    @classmethod
    def find_id_by_type_and_libelle(cls, type, libelle):
        return cls.query.filter_by(type=type, libelle=libelle).first()

    @classmethod
    def find_id_by_type_and_code(cls, type, code):
        return cls.query.filter_by(type=type, code=code).first()

    @classmethod
    def get_references(cls):
        result = defaultdict(list)
        for item in cls.query.all():
            result[ReferenceType.get_name(item.type)].append({
                "code": item.code,
                "libelle": item.libelle})
        return result

    @classmethod
    def get_reference_codes(cls):
        result = defaultdict(list)
        for item in cls.query.all():
            result[ReferenceType.get_name(item.type)].append(item.code)
        return result

    def __init__(self, type, code, libelle):
        self.type = type
        self.code = code
        self.libelle = libelle


class Address(db.Model, BaseModel):
    __tablename__ = 'orga_address'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    zipcode = db.Column(db.String(10))
    city = db.Column(db.String(50))
    lon = db.Column(db.Integer)
    lat = db.Column(db.Integer)

    organization = db.relationship("Organisation", uselist=False, back_populates="address")


class Organisation(db.Model, BaseModel):
    __tablename__ = 'orga_organization'

    id = db.Column(db.Integer, primary_key=True)
    vid = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(30))
    role = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    status = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    availability = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))


    address_id = db.Column(db.Integer, db.ForeignKey('orga_address.id'))
    address = db.relationship("Address", back_populates="organization")

   # This is used to discriminate between the linked tables.
    object_type = db.Column(db.Unicode(255))
    # This is used to point to the primary key of the linked row.
    object_id = db.Column(db.Integer)
    data = generic_relationship(object_type, object_id)

    users = db.relationship("User", back_populates="organization")


class Manufacturor(db.Model, BaseModel):
    __tablename__ = 'orga_manufacturor'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    capacity = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    skill_level = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    quality_need = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    contract_type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))


class Transporter(db.Model, BaseModel):
    __tablename__ = 'orga_transporter'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    capacity_type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    capacity_value = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    range_value = db.Column(db.Integer)
    range_type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))


class Provider(db.Model, BaseModel):
    __tablename__ = 'orga_provider'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    subtype = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))


class Customer(db.Model, BaseModel):
    __tablename__ = 'orga_customer'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    subtype = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
