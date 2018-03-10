from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from apps_base.order.models import Order
from apps_base.order.constants import PAGADO
from .constants import CULQI_VENTA_EXITOSA, ERROR_PEDIDO_PAGADO
from .utils import verify_charge
import culqipy
import json

culqipy.public_key = settings.ENV.get('CULQUI_PUBLIC_KEY_TEST')
culqipy.secret_key = settings.ENV.get('CULQUI_SECRET_KEY_TEST')


def save_token(request):
    data = {'status': 'error'}

    if request.is_ajax() and request.method == 'POST':
        code_cart = request.COOKIES.get('cart', None)
        if not Order.objects.filter(cart__code=code_cart).exists():
            return JsonResponse({}, status=404)
        _token = request.POST.get('token')
        token = json.loads(_token)
        status = token.get('object')
        if status == 'error':
            return JsonResponse(data, status=403)
        order = Order.objects.get(cart__code=code_cart)
        order.update_total()
        order_customer = order.order_order_customer
        order_shipping = order.order_ordershipping

        dir_charge = {
            'amount': int(order.total * 100),
            'currency_code': 'PEN',
            'description': 'Venta en Fanntop',
            'email': order_customer.email,
            'metadata': {'pedido': order.code},
            'source_id': token.get('id')
        }
        dir_charge['antifraud_details'] = {
            'first_name': order_customer.first_name[:25],
            'last_name': order_customer.last_name[:25],
            'phone_number': order_customer.phone,
            'address': order_shipping.address[:50],
            'address_city': order_shipping.ubigeo.full_ubigeo()[:50],
            'country_code': 'PE'
        }
        if order.type_status == PAGADO:
            data['msg'] = ERROR_PEDIDO_PAGADO
            return JsonResponse(data)
        charge = culqipy.Charge.create(dir_charge)
        response, id_charge = verify_charge(charge, order)
        order.extra_data = {
            'token_id': token.get('id'),
            'id_charge': id_charge
        }
        order.save()
        data.update(response)
    return JsonResponse(data)
