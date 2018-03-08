from .constants import PAGADO
import uuid

def generate_code_order():
    return 'order-' + str(uuid.uuid4()).replace("-", "")

def post_pago(order):
    order.type_status = PAGADO
    order.save()