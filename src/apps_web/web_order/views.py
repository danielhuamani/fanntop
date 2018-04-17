from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps_base.customers.models import CustomerShippingAddress, Customer
from apps_base.cart.models import Cart
from apps_base.order.models import Order, OrderShippingAddress, OrderCustomer
from apps_base.ubigeo.models import Ubigeo, Departamento
from apps_base.order.order import OrderGenerate
from apps_base.shipping.models import ShippingCost
from apps_base.promotion.models import CouponGenerate, Coupon
from django.db import transaction
from .forms import OrderCustomerForm, OrderShippingAddressForm
from decimal import Decimal as D


@login_required(login_url=reverse_lazy("web_system:login_register"))
@transaction.atomic
def checkout_paso_1(request):
    code_cart = request.COOKIES.get('cart', None)
    if not Cart.objects.filter(code=code_cart).exists():
        return redirect('web_system:home')
    else:
        cart = Cart.objects.prefetch_related('cart_items', 'cart_items__product',
            'cart_items__product__product_class').get(code=code_cart)
    user = request.user
    customer = user.user_customer
    code_departamento = ''
    code_provincia = ''
    code_distrito = ''
    existe_order = False
    sub_total = cart.total
    total = cart.total
    shipping_price = 0
    order = ''
    discount = 0
    coupon = request.COOKIES.get('coupon', None)
    if Order.objects.filter(cart__code=code_cart).exists():
        order_cart = Order.objects.get(cart__code=code_cart)
        order = order_cart
        order_shipping_instance = order_cart.order_ordershipping
        order_shipping_address = order_shipping_instance.shipping_address
        order_customer_instance = order_cart.order_order_customer
        ubigeo = order_shipping_instance.ubigeo
        code_departamento = ubigeo.cod_dep_inei
        code_provincia = ubigeo.cod_prov_inei
        code_distrito = ubigeo.pk
        existe_order = True
        discount = order.discount
        total = total + order.shipping_price - discount
        shipping_price = order.shipping_price
        form = OrderCustomerForm(prefix='customer', instance=order_customer_instance)
    else:
        order_shipping_instance = OrderShippingAddress()
        order_customer_instance = OrderCustomer()
        order_shipping_address = None
        initial = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'document': customer.document,
            'phone': customer.phone,
            'type_document': customer.type_document,
        }
        form = OrderCustomerForm(prefix='customer', initial=initial, instance=order_customer_instance)
    shipping_address = CustomerShippingAddress.objects.filter(customer=customer)
    distrito = []
    if request.method == 'POST':
        form = OrderCustomerForm(request.POST, prefix='customer', instance=order_customer_instance)
        form_order_shipping = OrderShippingAddressForm(request.POST, prefix='shipping', instance=order_shipping_instance)
        form_order_shipping.fields['direccion_save'].queryset = CustomerShippingAddress.objects.filter(customer=customer)
        provincia = request.POST.get('provincia')
        ubigeo = request.POST.get('shipping-ubigeo')
        if provincia:
            form_order_shipping.fields["ubigeo"].queryset = Ubigeo.objects.filter(
                cod_ubigeo_inei__startswith=provincia).order_by('desc_ubigeo_inei')

        if form.is_valid() and form_order_shipping.is_valid():
            data_shipping = form_order_shipping.cleaned_data
            order_generate = OrderGenerate()
            if existe_order:
                order = order_generate.update(cart, data_shipping.get('ubigeo'), coupon)
            else:
                order = order_generate.create(cart, customer, data_shipping.get('ubigeo'), coupon)
            form.instance.order = order
            order_customer = form.save()
            form_order_shipping.instance.order = order
            order_shipping = form_order_shipping.save()
            user.first_name = order_customer.first_name
            user.last_name = order_customer.last_name
            user.email = order_customer.email
            user.save()
            customer.phone = order_customer.phone
            customer.document = order_customer.document
            customer.type_document = order_customer.type_document
            customer.save()
            direccion_save = data_shipping.get('direccion_save')
            if not direccion_save:
                try:
                    customer_shipping = CustomerShippingAddress(
                        customer=customer,
                        first_name=order_shipping.first_name,
                        last_name=order_shipping.last_name,
                        type_document=order_shipping.type_document,
                        document=order_shipping.document,
                        phone=order_shipping.phone,
                        address=order_shipping.address,
                        reference=order_shipping.reference,
                        ubigeo=order_shipping.ubigeo,
                        order=order_shipping
                    )
                    customer_shipping.save()
                    order_shipping.shipping_address = customer_shipping
                    order_shipping.save()
                except Exception as e:
                    print(e, 'error')
            else:
                direccion_save.first_name = order_shipping.first_name
                direccion_save.last_name = order_shipping.last_name
                direccion_save.type_document = order_shipping.type_document
                direccion_save.document = order_shipping.document
                direccion_save.phone = order_shipping.phone
                direccion_save.address = order_shipping.address
                direccion_save.reference = order_shipping.reference
                direccion_save.ubigeo = order_shipping.ubigeo
                direccion_save.order = order_shipping
                direccion_save.save()
                order_shipping.shipping_address = direccion_save
                order_shipping.save()
            return redirect(reverse_lazy('web_order:checkout_paso_2'))

        else:
            print('invalid', form.errors, form_order_shipping.errors)
    else:
        form_order_shipping = OrderShippingAddressForm(prefix='shipping', instance=order_shipping_instance)
        form_order_shipping.fields['direccion_save'].queryset = CustomerShippingAddress.objects.filter(customer=customer)
        form_order_shipping.fields['direccion_save'].initial = order_shipping_address
    ctx = {
        'order': order,
        'cart': cart,
        'form': form,
        'total': total,
        'shipping_price': shipping_price,
        'discount': discount,
        'sub_total': sub_total,
        'form_order_shipping': form_order_shipping,
        'shipping_address': shipping_address,
        'distrito': distrito,
        'code_departamento': code_departamento,
        'code_provincia': code_provincia,
        'code_distrito': code_distrito
    }
    return render(request, "order/checkout_1.html", ctx)

# Create your views here.
@login_required(login_url=reverse_lazy("web_system:login_register"))
@transaction.atomic
def checkout_paso_2(request):
    code_cart = request.COOKIES.get('cart', None)

    if not Order.objects.filter(cart__code=code_cart).exists():
        return redirect('web_order:checkout_paso_1')
    order = Order.objects.get(cart__code=code_cart)
    order_details = order.order_orderdetail.all()
    order_customer = order.order_order_customer
    order_shipping = order.order_ordershipping
    order_total = int(order.total * 100)
    ctx = {
        'order': order,
        'order_total': order_total,
        'order_details': order_details,
        'order_customer': order_customer,
        'order_shipping': order_shipping,
        'CULQUI_PUBLIC_KEY_TEST': settings.CULQUI_PUBLIC_KEY_TEST
    }
    return render(request, "order/checkout_2.html", ctx)


@login_required(login_url=reverse_lazy("web_system:login_register"))
def checkout_thanks(request):
    code_cart = request.COOKIES.get('cart', None)
    if not Order.objects.filter(cart__code=code_cart).exists():
        return redirect('web_system:home')
    order = Order.objects.get(cart__code=code_cart)
    ctx = {
        'order': order
    }
    response = render(request, "order/checkout_thanks.html", ctx)
    response.delete_cookie('cart')
    return response


@login_required(login_url=reverse_lazy("web_system:login_register"))
def get_price_shipping(request):
    ubigeo = request.GET.get('ubigeo', None)
    data = {
        'price': float(0)
    }
    if ubigeo:
        shipping = ShippingCost.objects.filter(ubigeo_id=int(ubigeo))
        if shipping.exists():
            price = shipping.first().price
            data['price'] = price
    return JsonResponse(data, status=200)


@login_required(login_url=reverse_lazy("web_system:login_register"))
def get_coupon_discount(request):
    coupon = request.GET.get('coupon', None)
    code_cart = request.COOKIES.get('cart', None)
    cart = Cart.objects.get(code=code_cart)
    sub_total = cart.total
    total = cart.total
    order = None
    total = cart.total
    shipping_price = 0
    try:
        order = Order.objects.get(cart__code=code_cart)
        shipping_price = order.shipping_price
        total = total + order.shipping_price
    except Exception as e:
        print(e, 'nivel')
    data = {
        'status': 'error'
    }
    if coupon:
        try:
            coupon_generate = Coupon.objects.get(
                prefix=coupon.strip(), is_active=True)
            if not Order.objects.filter(coupon_discount__prefix=coupon.strip()).exists():
                if coupon_generate.type_discount == 'PTJ':
                    discount = (float(float(sub_total)*coupon_generate.discount) / 100)
                elif coupon_generate.type_discount == 'SLS':
                    discount = coupon_generate.discount
                if order:
                    total = total - D(discount)
                    order.discount = discount
                    order.coupon_discount = coupon_generate
                    order.total = total
                    order.save()
                    data['discount'] = D(discount)
                    data['shipping_price'] = shipping_price
                    data['total'] = total
                    data['sub_total'] = sub_total
                    data['status'] = 'ok'
                else:
                    data['discount'] = D(discount)
                    data['shipping_price'] = shipping_price
                    data['total'] = total
                    data['sub_total'] = sub_total
                    data['status'] = 'ok'
            else:
                data['msj'] = 'Este cupon ya ha sido usado'
        except Exception as e:
            print(e, 'error')
            data['msj'] = 'Este cupon no existe'
            return JsonResponse(data, status=200)
    response = JsonResponse(data, status=200)
    response.set_cookie('coupon', coupon, max_age=60*60*24*2)
    return response