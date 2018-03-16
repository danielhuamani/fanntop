from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from apps_base.pages.models import HomeBanner
from apps_base.influencer.models import Influencer
from django.contrib.auth.forms import AuthenticationForm
from apps_base.custom_auth.models import User
from apps_base.ubigeo.models import Ubigeo
from apps_base.order.models import Order
from apps_base.customers.models import CustomerShippingAddress
from django.db import transaction
from .forms import UserRegisterForm, CustomerForm, UserUpdateForm, CustomerShippingAddressForm
from .constants import REGISTER, LOGIN
from .utils import send_mail_customer_welcome


def home(request):
    home_banners = HomeBanner.objects.active()
    influencers = Influencer.objects.active().order_by('position')
    ctx = {
        'home_banners': home_banners,
        'influencers': influencers
    }
    return render(request, "system/home.html", ctx)

@transaction.atomic
def login_register(request):
    if request.method == 'POST':
        form_register = UserRegisterForm(prefix='register')
        form_login = AuthenticationForm(prefix='login')
        if request.POST.get('type_submit') == REGISTER:
            form_register = UserRegisterForm(request.POST, prefix='register')
            if form_register.is_valid():
                user_register = form_register.save()
                username = user_register.email
                raw_password = form_register.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                send_mail_customer_welcome(user_register)
                auth_login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect(reverse_lazy('web_system:account'))
            else:
                print(form_register.errors)
        elif request.POST.get('type_submit') == LOGIN:
            form_login = AuthenticationForm(request, data=request.POST, prefix='login')
            if form_login.is_valid():
                auth_login(request, form_login.get_user())
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect(reverse_lazy('web_system:account'))
    else:
        form_register = UserRegisterForm(prefix='register')
        form_login = AuthenticationForm(prefix='login')
    ctx = {
        'form_register': form_register,
        'form_login': form_login,
        'LOGIN': LOGIN,
        'REGISTER': REGISTER
    }
    return render(request, "system/login_register.html", ctx)

@login_required(login_url=reverse_lazy("web_system:login_register"))
def account(request):
    user = request.user
    print(user, 'user')
    customer = user.user_customer
    if request.method == 'POST':
        form_customer = CustomerForm(request.POST, instance=customer)
        form_user = UserUpdateForm(request.POST, instance=user)
        if form_customer.is_valid() and form_user.is_valid():
            print('valid')
            form_customer.save()
            form_user.save()
            return redirect(reverse('web_system:account'))

    else:
        form_customer = CustomerForm(instance=customer)
        form_user = UserUpdateForm(instance=user)
    ctx = {
        'form_customer': form_customer,
        'form_user': form_user
    }
    return render(request, "system/account.html", ctx)

@login_required(login_url=reverse_lazy("web_system:login_register"))
def my_order(request):
    user = request.user
    customer = user.user_customer
    orders = Order.objects.filter(customer=customer)
    ctx = {
        'user': user,
        'orders': orders
    }
    return render(request, "system/my_order.html", ctx)

@login_required(login_url=reverse_lazy("web_system:login_register"))
def my_order_detail(request, pk):
    user = request.user
    customer = user.user_customer
    order = get_object_or_404(Order, customer=customer, pk=pk)
    order_customer = order.order_order_customer
    order_shipping = order.order_ordershipping
    order_products = order.order_orderdetail.all()
    ctx = {
        'order': order,
        'order_customer': order_customer,
        'order_shipping': order_shipping,
        'order_products': order_products
    }
    return render(request, "system/my_order_detail.html", ctx)

@login_required(login_url=reverse_lazy("web_system:login_register"))
def my_address(request):
    user = request.user
    customer = user.user_customer
    address = customer.customer_shipping_address.all()
    ctx = {
        'user': user,
        'address': address
    }
    return render(request, "system/my_address.html", ctx)


@login_required(login_url=reverse_lazy("web_system:login_register"))
def my_address_edit(request, pk):
    user = request.user
    customer = user.user_customer
    address_detail = get_object_or_404(CustomerShippingAddress, customer=customer, pk=pk)
    ubigeo = address_detail.ubigeo
    code_departamento = ubigeo.cod_dep_inei
    code_provincia = ubigeo.cod_prov_inei
    code_distrito = ubigeo.pk

    if request.method == 'POST':
        form = CustomerShippingAddressForm(request.POST, instance=address_detail)
        provincia = request.POST.get('provincia')
        ubigeo = request.POST.get('ubigeo')
        if provincia:
            form.fields["ubigeo"].queryset = Ubigeo.objects.filter(
                cod_ubigeo_inei__startswith=provincia).order_by('desc_ubigeo_inei')
        if form.is_valid():
            form.save()
            return redirect(reverse('web_system:my_address'))
    else:
        form = CustomerShippingAddressForm(instance=address_detail)
    ctx = {
        'form': form,
        'code_departamento': code_departamento,
        'code_provincia': code_provincia,
        'code_distrito': code_distrito
    }
    return render(request, "system/my_address_edit.html", ctx)


@login_required(login_url=reverse_lazy("web_system:login_register"))
def my_address_create(request):
    user = request.user
    customer = user.user_customer
    # ubigeo = address_detail.ubigeo
    # code_departamento = ubigeo.cod_dep_inei
    # code_provincia = ubigeo.cod_prov_inei
    # code_distrito = ubigeo.pk

    # ubigeo = address_detail.ubigeo
    code_departamento = ''
    code_provincia = ''
    code_distrito = ''
    if request.method == 'POST':
        form = CustomerShippingAddressForm(request.POST)
        provincia = request.POST.get('provincia')
        ubigeo = request.POST.get('ubigeo')
        if provincia:
            form.fields["ubigeo"].queryset = Ubigeo.objects.filter(
                cod_ubigeo_inei__startswith=provincia).order_by('desc_ubigeo_inei')
        if form.is_valid():
            form.instance.customer = customer
            form.save()
            return redirect(reverse('web_system:my_address'))
    else:
        form = CustomerShippingAddressForm()
    ctx = {
        'form': form,
        # 'code_departamento': code_departamento,
        # 'code_provincia': code_provincia,
        # 'code_distrito': code_distrito
    }
    return render(request, "system/my_address_create.html", ctx)


def test_email(request):
    user = User.objects.get(email='danielhuamani15@gmail.com')
    send_mail_customer_welcome(user)
    ctx = {}
    return render(request, "system/account.html", ctx)

def logout_view(request):
    logout(request)
    response = redirect("web_system:home")
    response.delete_cookie('cart')

    return response