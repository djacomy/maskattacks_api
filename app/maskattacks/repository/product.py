import constant
from uuid import uuid4

from sqlalchemy import *

from maskattacks.model.product import *
from maskattacks.model.orga import Organisation
from maskattacks.util.validator import get_error_messages


class ProductException(Exception):

    def __init__(self, msg,  details):
        super(ProductException, self).__init__(msg)
        self.msg = msg
        self.details = details


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


def count_all_stocks_by_reference_and_type(page=1, limit=10):
    return db.session.query(Product.reference, Stock.type, func.sum(Stock.count))\
        .join(Stock, Stock.product_id == Product.id)\
        .group_by(Product.reference, Stock.type)\
        .paginate(page, limit)


def count_all_delivery_by_reference_and_type(page=1, limit=10):
    """

    :param offset:
    :param limit:
    :return: Iterator
    """
    return db.session.query(Product.reference, Organisation.name,  DeliveryItem.type, DeliveryItem.status, func.sum(DeliveryItem.count))\
        .join(DeliveryItem, DeliveryItem.product_id == Product.id)\
        .join(Organisation, Organisation.id == DeliveryItem.manufactor_id)\
        .group_by(Product.reference, Organisation.name, DeliveryItem.type, DeliveryItem.status)\
        .paginate(page, limit)


def list_all_batch_by_destination(page=1, limit=10):
    """

    :param offset:
    :param limit:
    :return:  Iterator
    """
    return db.session.query(Batch.id, Organisation.name,  Batch.status, Batch.count)\
        .join(Organisation, Organisation.id == Batch.destination_id)\
        .paginate(page, limit)


def count_stock_by_reference(reference):
    obj = db.session.query(Product.reference, func.sum(Stock.count))\
        .join(Stock, Stock.product_id == Product.id)\
        .filter(Product.reference == reference).group_by(Product.reference).first()
    if obj is None:
        return 0
    return obj[1]


def get_stock_by_reference(reference):
    obj = db.session.query(Product.reference, Stock.type, func.sum(Stock.count))\
        .join(Stock, Stock.product_id == Product.id)\
        .filter(Product.reference == reference).group_by(Product.reference, Stock.type).first()
    if obj is None:
        return

    return {
        "reference": obj[0],
        "type": ProductType.get_name(obj[1]),
        "count": obj[2]
    }


def get_deliveryitem_by_reference(reference):
    obj = db.session.query(Product.reference,  DeliveryItem.type, DeliveryItem.status, Organisation.name, func.sum(DeliveryItem.count))\
        .join(DeliveryItem, DeliveryItem.product_id == Product.id) \
        .join(Organisation, DeliveryItem.manufactor_id == Organisation.id) \
        .filter(Product.reference == reference).group_by(Product.reference, DeliveryItem.type, DeliveryItem.status,Organisation.name).all()
    if not obj:
        return

    return {
        "reference": reference,
        "deliveries": [{"type": ProductType.get_name(item[1]),
                        "status":  StatusType.get_name(item[2]),
                        "manufactor": item[3],
                        "count": item[4]} for item in obj]
    }


def count_delivery_by_reference_and_type(reference, delivery_type):
    obj = db.session.query(Product.reference, func.sum(DeliveryItem.count))\
        .join(DeliveryItem, DeliveryItem.product_id == Product.id)\
        .filter(and_(Product.reference == reference, DeliveryItem.type == delivery_type ))\
        .group_by(Product.reference).first()
    if obj is None:
        return 0
    return obj[1]


def list_stocks_by_reference(reference):
    return Stock.query\
        .join(Product, aliased=True)\
        .filter(Product.reference == reference).order_by(Stock.created_at)


def check_kit_stock_creation(ref, count):
    assert isinstance(ref, Product) == True
    assert ref.type == ProductType.final

    # checker si le stock des materiaux existe.
    # checker si il est en nombre suffisant.
    errors = []
    for item in ref.materials:
        mat_stock = count_stock_by_reference(item.reference)
        if not mat_stock:
            errors.append(get_error_messages(constant.NO_STOCK, item.reference))
            continue
        if item.material[0].count * count > mat_stock:
            errors.append(get_error_messages(constant.NOT_ENOUGH_STOCK, item.reference))
            continue
    if errors:
        raise ProductException("BAD_STOCK", errors)

    return True


def check_kit_delivery_creation(ref, expected):
    assert isinstance(ref, Product) == True
    assert ref.type == ProductType.final

    # checker si le stock des materiaux existe.
    # checker si il est en nombre suffisant.
    errors = []
    stock = count_stock_by_reference(ref.reference)
    if not stock:
        errors.append(get_error_messages(constant.NO_STOCK, ref.reference))

    if expected > stock:
        errors.append(get_error_messages(constant.NOT_ENOUGH_STOCK, ref.reference))
    if errors:
        raise ProductException("BAD_STOCK", errors)

    return True


def create_product_reference(product_type, reference, libelle):

    if product_type == ProductType.kit:
        raise ValueError("Type cannot be a kit.")

    req = Product(reference=reference, type=product_type, libelle=libelle)
    req.save()
    return req


def create_material_stock(ref, count, *args):
    """

    :param reference:
    :param count:
    :return:
    """
    assert isinstance(ref, Product) == True
    assert ref.type == ProductType.materials

    req = Stock(product=ref, type=ref.type, count=count)
    req.save()
    return req


def create_kit_stock(ref, count, *args):
    """

    :param ref:
    :param count:
    :return:
    """
    assert isinstance(ref, Product) == True
    assert ref.type == ProductType.final

    # update stock materials
    stock_to_save = []
    stock_to_remove = []
    for item in ref.materials:
        expected = item.material[0].count * count
        for stock in list_stocks_by_reference(item.reference):
            if stock.count > expected:
                stock.count -= expected
                stock_to_save.append(stock)
            else:
                # stock to go to 0 remove it after decrement
                stock_to_remove.append(stock)

            expected -= stock.count

    # save
    [it.save() for it in stock_to_save]
    # remove empty material stock
    [it.remove() for it in stock_to_remove]

    # create kit stock
    req = Stock(product=ref, type=ProductType.kit, count=count)
    req.save()

    return req


def create_kit_delivery_stock(ref, expected, man):
    assert isinstance(ref, Product) == True
    assert ref.type == ProductType.final
    assert isinstance(man, Organisation) == True
    assert man.role_obj.code == "man"

    stock_to_remove = []
    stock_to_save = []
    count = expected
    for stock in list_stocks_by_reference(ref.reference).all():
        if stock.count >= count:
            stock.count -= count
            stock_to_save.append(stock)
        else:
            # stock to go to 0 remove it after decrement
            stock_to_remove.append(stock)

        count -= stock.count

    [it.save() for it in stock_to_remove]
    # remove empty material stock
    [it.remove() for it in stock_to_remove]

    # create kit delivery item
    req = DeliveryItem(product=ref, manufactor=man, type=ProductType.kit, count=expected)
    req.save()

    return req


def create_final_delivery_stock(ref, expected, man):
    assert isinstance(ref, Product) == True
    assert ref.type == ProductType.final
    assert isinstance(man, Organisation) == True
    assert man.role_obj.code == "man"

    # create product delivery item
    req = DeliveryItem(product=ref, manufactor=man, type=ProductType.final, count=expected)
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
            batch = Batch(count=batch_size, destination=obj.manufactor, deliveryitem=obj, reference=uuid4())
        else:
            batch = Batch(count=batch_size, deliveryitem=obj, reference=uuid4())
        batch.save()
        count -= batch_size

    if count > 0:
        if obj.type == ProductType.kit:
            batch = Batch(count=count, destination=obj.manufactor, deliveryitem=obj, reference=uuid4())
        else:
            batch = Batch(count=count, deliveryitem=obj, reference=uuid4())
        batch.save()
