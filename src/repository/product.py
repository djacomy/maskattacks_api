import constant

from sqlalchemy import *
from model.product import *
from model.orga import Organisation
from repository import reference as ref_repository
from repository import orga as orga_repository

from util.validator import get_error_messages


class ProductException(Exception):

    def __init__(self, msg,  details):
        super(ProductException, self).__init__(msg)
        self.msg = msg
        self.details = details


def create_product_reference(product_type, reference, libelle):

    if product_type == ProductType.kit:
        raise ValueError("Type cannot be a kit.")

    req = Product(reference=reference, type=product_type, libelle=libelle)
    req.save()
    return req


def list_product_references(page, pernumber=10):
    return [item.to_json() for item in Product.query.paginate(page, per_page=pernumber).items]


def get_product_reference_by_reference(ref):
    return Product.query.filter(Product.reference == ref).first()


def create_equivalence(product, reference_material, count):
    assert True == isinstance(product, Product)
    material = get_product_reference_by_reference(reference_material)

    eq = ProductEquivalence(product=product, material=material, count=count)
    eq.save()
    return eq


def create_material_stock(reference, count):
    """

    :param reference:
    :param count:
    :return:
    """
    ref = get_product_reference_by_reference(reference)
    if not ref:
        raise ValueError("Unknown reference")

    if ref.type != ProductType.materials:
        raise ValueError("The product reference should be a reference one. ")

    req = Stock(product=ref, type=ref.type, count=count)
    req.save()
    return req


def count_all_stocks_by_reference_and_type():
    obj = db.session.query(Product.reference, Stock.type, func.sum(Stock.count))\
        .join(Stock, Stock.product_id == Product.id).group_by(Product.reference, Stock.type).all()
    return obj


def count_all_delivery_by_reference_and_type():
    obj = db.session.query(Product.reference, Organisation.name,  DeliveryItem.type, func.sum(DeliveryItem.count))\
        .join(DeliveryItem, DeliveryItem.product_id == Product.id)\
        .join(Organisation, Organisation.id == DeliveryItem.manufactor_id)\
        .group_by(Product.reference, Organisation.name, DeliveryItem.type).all()
    return obj


def list_all_batch_by_destination():
    return db.session.query(Batch.id, Organisation.name,  Batch.status, Batch.count)\
        .join(Organisation, Organisation.id == Batch.destination_id).all()


def count_stock_by_reference(reference):
    obj = db.session.query(Product.reference, func.sum(Stock.count))\
        .join(Stock, Stock.product_id == Product.id)\
        .filter(Product.reference == reference).group_by(Product.reference).first()
    if obj is None:
        return 0
    return obj[1]


def list_stocks_by_reference(reference):
    return Stock.query\
        .join(Product, aliased=True)\
        .filter(Product.reference == reference).order_by(Stock.created_at)


def check_kit_stock_creation(reference, count):
    ref = get_product_reference_by_reference(reference)
    if not ref:
        raise ValueError("Unknown reference")

    if ref.type != ProductType.final:
        raise ValueError("The product reference should be a final one.")

    # checker si le stock des materiaux existe.
    # checker si il est en nombre suffisant.
    errors = []
    for item in ref.materials:
        mat_stock = count_stock_by_reference(item.reference)
        if not mat_stock:
            errors.append(f"No stock for reference {item.reference}")
            continue
        if item.material[0].count * count < mat_stock:
            errors.append(f"Not enough stock for reference {item.reference}")
            continue
    if errors:
        raise ProductException("BAD_STOCK", errors)

    return True


def create_kit_stock(reference, count):
    ref = get_product_reference_by_reference(reference)
    if not ref:
        raise ValueError("Unknown reference")

    if ref.type != ProductType.final:
        raise ValueError("The product reference should be a final one.")

    # update stock materials
    stock_to_remove = []
    for item in ref.materials:
        expected = item.material[0].count * count
        for stock in list_stocks_by_reference(item.reference):
            if stock.count > expected:
                stock.count -= expected
            else:
                # stock to go to 0 remove it after decrement
                stock_to_remove.append(stock)

            expected -= stock.count

    # remove empty material stock
    [it.remove() for it in stock_to_remove]

    # create kit stock
    req = Stock(product=ref, type=ProductType.kit, count=count)
    req.save()

    return req


def create_kit_delivery_creation(reference, vid,  expected):
    ref = get_product_reference_by_reference(reference)
    if not ref:
        raise ValueError("Unknown reference")

    if ref.type != ProductType.final:
        raise ValueError("The product reference should be a final one.")

    manufactor = orga_repository.get_organisation(vid)
    if not  manufactor:
        raise ValueError("Organization not found.")

    if manufactor.role_obj.code != "man":
        raise ValueError("Organization is not a manufactor.")

    # checker si le stock des materiaux existe.
    # checker si il est en nombre suffisant.
    errors = []
    stock = count_stock_by_reference(ref.reference)
    if not stock:
        errors.append(f"No stock for reference {ref.reference}")

    if stock < expected:
        errors.append(f"Not enough stock for reference {ref.reference}")
    if errors:
        raise ProductException("BAD_STOCK", errors)

    stock_to_remove = []
    count = expected
    for stock in list_stocks_by_reference(ref.reference).all():
        if stock.count >= count:
            stock.count -= count
        else:
            # stock to go to 0 remove it after decrement
            stock_to_remove.append(stock)

        count -= stock.count

        # remove empty material stock
    [it.remove() for it in stock_to_remove]

    # create kit delivery item
    req = DeliveryItem(product=ref, manufactor=manufactor, type=ProductType.kit, count=expected)
    req.save()

    return req


def create_final_delivery_stock(reference, vid,  expected):
    ref = get_product_reference_by_reference(reference)
    if not ref:
        raise ValueError("Unknown reference")

    if ref.type != ProductType.final:
        raise ValueError("The product reference should be a final one.")

    manufactor = orga_repository.get_organisation(vid)
    if not manufactor:
        raise ValueError("Organization not found.")

    if manufactor.role_obj.code != "man":
        raise ValueError("Organization is not a manufactor.")

    # create product delivery item
    req = DeliveryItem(product=ref, manufactor=manufactor, type=ProductType.final, count=expected)
    req.save()

    return req


def generate_batch_from_delivery_item(id, batch_size):

    obj = DeliveryItem.query.get(id)
    if not obj:
        raise ValueError("No delivery item found.")

    nb = len(obj.batches)
    if nb > 0:
        raise ValueError("Delivery item has already been packaged.")

    count = obj.count
    for i in range(0, int(obj.count / batch_size)):
        if obj.type == ProductType.kit:
            batch = Batch(count=batch_size, destination=obj.manufactor)
        else:
            batch = Batch(count=batch_size)
        batch.save()
        obj.batches.append(batch)
        count -= batch_size

    if count > 0:
        if obj.type == ProductType.kit:
            batch = Batch(count=count, destination=obj.manufactor)
        else:
            batch = Batch(count=count)
        batch.save()
        obj.batches.append(batch)
    obj.save()

