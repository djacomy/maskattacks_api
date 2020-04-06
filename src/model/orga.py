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

    to_json_filter = ('id', "organization", )

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
    role_obj = db.relationship(Reference, foreign_keys=[role])
    status = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    status_obj = db.relationship(Reference, foreign_keys=[status])
    availability = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    availability_obj = db.relationship(Reference, foreign_keys=[availability])

    address_id = db.Column(db.Integer, db.ForeignKey('orga_address.id'))
    address = db.relationship(Address, back_populates="organization")

   # This is used to discriminate between the linked tables.
    object_type = db.Column(db.Unicode(255))
    # This is used to point to the primary key of the linked row.
    object_id = db.Column(db.Integer)

    data = generic_relationship(object_type, object_id)

    users = db.relationship("User", back_populates="organization")

    @property
    def json(self):
        return {
            "id": self.id,
            "vid": self.vid,
            "role":  self.role_obj.code,
            'status': self.status_obj.code,
            'availability': self.availability_obj.code,
            "address": self.address.json,
            "data": self.data.json
        }


class Manufacturor(db.Model, BaseModel):
    __tablename__ = 'orga_manufacturor'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    capacity = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    skill_level = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    quality_need = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    contract_type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))

    type_obj = db.relationship(Reference, foreign_keys=[type])
    capacity_obj = db.relationship(Reference, foreign_keys=[capacity])
    skill_level_obj = db.relationship(Reference, foreign_keys=[skill_level])
    contract_type_obj = db.relationship(Reference, foreign_keys=[contract_type])

    @property
    def json(self):
        return {
            "type": self.type_obj.code,
            "capacity":  self.capacity_obj.code,
            'skill_level': self.skill_level_obj.code,
            'contract_type': self.contract_type_obj.code,
        }


class Transporter(db.Model, BaseModel):
    __tablename__ = 'orga_transporter'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    capacity_type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    capacity_value = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    range_value = db.Column(db.Integer)
    range_type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))

    type_obj = db.relationship(Reference, foreign_keys=[type])
    capacity_type_obj = db.relationship(Reference, foreign_keys=[capacity_type])
    capacity_value_obj = db.relationship(Reference, foreign_keys=[capacity_value])
    range_type_obj = db.relationship(Reference, foreign_keys=[range_type])

    @property
    def json(self):
        return {
            "type": self.type_obj.code,
            "capacity":{
                "type": self.capacity_type.code,
                "value": self.capacity_type.value,
            } ,
            'range': {
                "type": self.range_type.code,
                "value": self.range_value,
            }
        }


class Provider(db.Model, BaseModel):
    __tablename__ = 'orga_provider'

    to_json_filter =  ('type', 'subtype', )

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    subtype = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    type_obj = db.relationship(Reference, foreign_keys=[type])
    subtype_obj = db.relationship(Reference, foreign_keys=[subtype])

    @property
    def json(self):
        return {
            "type": self.type_obj.code,
            "subtype": self.subtype_obj.code,
        }


class Customer(db.Model, BaseModel):
    __tablename__ = 'orga_customer'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    subtype = db.Column(db.Integer, db.ForeignKey("orga_reference.id"))
    type_obj = db.relationship(Reference, foreign_keys=[type])
    subtype_obj = db.relationship(Reference, foreign_keys=[subtype])

    @property
    def json(self):
        return {
            "type": self.type_obj.code,
            "subtype": self.subtype_obj.code,
        }
