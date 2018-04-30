from .constants import PAGADO
from django.db import transaction
from apps_base.cart.constants import DANGER
import uuid

def generate_code_order():
    from apps_base.order.models import Order

    try:
        last_id = Order.objects.all().last().id
    except Exception as e:
        last_id = 0
    last_id = last_id + 1
    return str(last_id).zfill(8)

def validate_stock(order):
    stock = True
    for order_detail in order.order_orderdetail.all().prefetch_related('productdetail'):
        if order_detail.quantity > order_detail.productdetail.stock:
            cart_detail = order.cart.cart_items.filter(product=order_detail.productdetail).first()
            cart_detail.extra_data = {
                'msj': 'No contamos con el stock',
                'status': DANGER
            }
            cart_detail.save()
            stock = False
    if not stock:
        cart = order.cart
        cart.extra_data = {
            'msj': 'Uno de los productos se quedó sin stock'
        }
        cart.save()
    return stock

def discount_stock_order(order):
    with transaction.atomic():
        for order_detail in order.order_orderdetail.all():
            product_detail = order_detail.productdetail
            product_detail.stock = product_detail.stock - order_detail.quantity
            product_detail.save()

def post_pago(order):
    order.discount_stock = True
    order.type_status = PAGADO
    order.save()
    discount_stock_order(order)