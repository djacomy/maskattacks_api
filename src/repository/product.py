from sqlalchemy import *
from model.product import *
from repository import reference as ref_repository
from repository import orga as orga_repository


class ProductException(Exception):

    def __init__(self, msg,  details):
        super(ProductException, self).__init__(msg)
        self.msg = msg
        self.details = details


def create_product_reference(product_type, reference, libelle):
    if not isinstance(product_type, ProductType):
        raise ValueError("Type should be a instance of product type.")

    if product_type == ProductType.kit:
        raise ValueError("Type cannot be a kit.")

    req = Product(reference=reference, type=product_type, libelle=libelle)
    req.save()
    return req


def get_product_reference_by_reference(ref):
    return Product.query.filter(Product.reference == ref).first()


def create_equivalence(product, reference_material, count):
    if not isinstance(product, Product):
        raise ValueError("product should be a Product instance")
    material = get_product_reference_by_reference(reference_material)
    if not material:
        raise ValueError("Unknown reference")

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
