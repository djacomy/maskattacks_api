import enum
from datetime import datetime
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
from .abc import db, BaseModel
from model.orga import Organisation


class StatusType(enum.Enum):
    submitted = "submitted"
    running = "running"
    delivered = "delivered"

    @classmethod
    def get_value(cls, name):
        return getattr(cls, name).value

    @classmethod
    def get_name(cls, value):
        return cls(value).name


class ProductType(enum.IntEnum):
    materials = 1
    kit = 2
    final = 3

    @classmethod
    def get_value(cls, name):
        return getattr(cls, name).value

    @classmethod
    def get_name(cls, value):
        return cls(value).name


class ProductEquivalence(db.Model, BaseModel):
    __tablename__ = 'product_equivalence'
    __table_args__ = {'extend_existing': True}

    to_json_filter = ('product', 'materials',)
    print_filter = ('product', 'material',)

    product_id = db.Column(db.Integer, db.ForeignKey('product_product.id'), primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('product_product.id'), primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    product = relationship("Product", foreign_keys=[product_id])
    material = relationship("Product", foreign_keys=[material_id], uselist=False,  backref="material")


class Product(db.Model, BaseModel):
    __tablename__ = 'product_product'

    to_json_filter = ('materials', 'material', "created_at",)
    print_filter = ('materials', 'material')

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reference = db.Column(db.String(25), nullable=False, unique=True)
    type = db.Column(
        ChoiceType(ProductType, impl=db.Integer()),
        nullable=False
    )

    libelle = db.Column(db.String(25), nullable=True)
    materials = relationship('Product', secondary=lambda: ProductEquivalence.__table__,
                             primaryjoin=(ProductEquivalence.product_id == id),
                             secondaryjoin=(ProductEquivalence.material_id == id),
                             )

    def to_json(self):
        p = self.json
        p["type"] = ProductType.get_name(p["type"])
        if self.type != ProductType.final:
            return p
        lst = []
        for item in self.materials:
            tmp = item.json
            tmp["type"] = ProductType.get_name(tmp["type"])
            tmp["count"] = item.material[0].count
            lst.append(tmp)
        p["materials"] = lst
        return p


class Stock(db.Model, BaseModel):
    __tablename__ = 'product_stock'

    to_json_filter = ('id', "product_type_id", "product_type_id", 'product', )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    type = db.Column(
        ChoiceType(ProductType, impl=db.Integer()),
        nullable=False
    )

    product_id = db.Column(db.Integer, db.ForeignKey("product_product.id"), nullable=False)
    product = db.relationship(Product, foreign_keys=[product_id])

    count = db.Column(db.Integer, default=0, nullable=False)

    def to_json(self):
        return {
            "reference": self.product.reference,
            "type": ProductType.get_name(self.type),
            "count": self.count
        }


class DeliveryItemBatch(db.Model, BaseModel):
    __tablename__ = 'product_deliveryitem_batch'

    batch_id = db.Column(db.Integer, db.ForeignKey('product_batch.id'), primary_key=True)
    deliveryitem_id = db.Column(db.Integer, db.ForeignKey('product_deliveryitem.id'), primary_key=True)

    deliveryitem = relationship("DeliveryItem", foreign_keys=[deliveryitem_id], backref="deliveryitem_items")
    batch = relationship("Batch", foreign_keys=[batch_id], backref="batch_items")


class DeliveryItem(db.Model, BaseModel):
    __tablename__ = 'product_deliveryitem'

    to_json_filter = ('id',  )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    type = db.Column(
        ChoiceType(ProductType, impl=db.Integer()),
        nullable=False
    )

    product_id = db.Column(db.Integer, db.ForeignKey("product_product.id"), nullable=False)
    product = db.relationship(Product, foreign_keys=[product_id])

    manufactor_id = db.Column(db.Integer, db.ForeignKey("orga_organization.id"), nullable=False)
    manufactor = db.relationship(Organisation, foreign_keys=[manufactor_id])

    status = db.Column(
        ChoiceType(StatusType, impl=db.String(15)),
        default=StatusType.submitted,
        nullable=False
    )

    count = db.Column(db.Integer, default=0, nullable=False)

    batches = relationship('Batch', secondary=lambda: DeliveryItemBatch.__table__,
                           primaryjoin=(DeliveryItemBatch.deliveryitem_id == id),
                           secondaryjoin=('DeliveryItemBatch.batch_id == Batch.id'),
                           )


class Batch(db.Model, BaseModel):
    __tablename__ = 'product_batch'

    to_json_filter = ('id', )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    count = db.Column(db.Integer, default=0, nullable=False)

    status = db.Column(
        ChoiceType(StatusType, impl=db.String(15)),
        default=StatusType.submitted,
        nullable=False
    )

    transporter_id = db.Column(db.Integer, db.ForeignKey("orga_organization.id"), nullable=True)
    transporter = db.relationship(Organisation, foreign_keys=[transporter_id])

    # from provider or manufactor
    destination_id = db.Column(db.Integer, db.ForeignKey("orga_organization.id"), nullable=True)
    destination = db.relationship(Organisation, foreign_keys=[destination_id])


