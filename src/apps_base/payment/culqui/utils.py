from .constants import ERRORES_CULQI, CULQI_VENTA_EXITOSA
from apps_base.order.utils import post_pago

def verify_charge(charge, order):
    response = {'status': 'error'}
    if charge.get('object') == 'error':
        if ERRORES_CULQI.get(charge.get('type')):
            response['msg'] = ERRORES_CULQI.get(charge.get('type'))
        else:
            response['msg'] = charge.get('user_message')
    if charge.get('outcome'):
        if charge.get('outcome').get('type') == CULQI_VENTA_EXITOSA:
            response['status'] = 'ok'
            post_pago(order)
    return response,  charge.get('id')


