from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps_base.customers.models import CustomerShippingAddress
from apps_base.cart.models import Cart
from apps_base.order.models import Order
from apps_base.ubigeo.models import Ubigeo, Departamento
from apps_base.order.order import OrderGenerate
from django.db import transaction
from .forms import OrderCustomerForm, OrderShippingAddressForm



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
    if Order.objects.filter(cart__code=code_cart).exists():
        form = OrderCustomerForm(prefix='customer')
    else:
        initial = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'document': customer.document,
            'phone': customer.phone,
            'type_document': customer.type_document,
        }
        form = OrderCustomerForm(prefix='customer', initial=initial)
    shipping_address = CustomerShippingAddress.objects.filter(customer=customer)

    if request.method == 'POST':
        form = OrderCustomerForm(request.POST, prefix='customer')
        form_order_shipping = OrderShippingAddressForm(request.POST, prefix='shipping')
        provincia = request.POST.get('provincia')
        if provincia:
            form_order_shipping.fields["ubigeo"].queryset = Ubigeo.objects.filter(cod_ubigeo_inei__startswith=provincia).order_by('desc_ubigeo_inei')
        if form.is_valid() and form_order_shipping.is_valid():
            data_shipping = form_order_shipping.cleaned_data
            order_generate = OrderGenerate()
            order = order_generate.create(cart, customer)
            form.instance.order = order
            form.save()
            form_order_shipping.instance.order = order
            form_order_shipping.save()
            if data_shipping.get('direccion_save'):
                try:
                    customer_shipping = CustomerShippingAddress(
                        customer=customer,
                        first_name=form_order_shipping.first_name,
                        last_name=form_order_shipping.last_name,
                        type_document=form_order_shipping.type_document,
                        document=form_order_shipping.document,
                        phone=form_order_shipping.phone,
                        address=form_order_shipping.address,
                        reference=form_order_shipping.reference,
                        ubigeo=form_order_shipping.ubigeo,
                        order=order,
                    )
                    customer_shipping.save()
                except Exception as e:
                    print(e, 'error')
            return redirect(reverse_lazy('web_order:checkout_paso_2'))

        else:
            print('invalid', form.errors, form_order_shipping.errors)
    else:
        form_order_shipping = OrderShippingAddressForm(request.POST, prefix='shipping')
    ctx = {
        'cart': cart,
        'form': form,
        'form_order_shipping': form_order_shipping,
        'shipping_address': shipping_address
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
    return render(request, "order/checkout_thanks.html", ctx)
