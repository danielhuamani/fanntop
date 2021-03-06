from django.conf.urls import url
from .views import (home, login_register, account, test_email,
    logout_view, my_address, my_address_edit, my_order, my_order_detail, my_address_create,
    follow_orders, testing_view, edit_profle)
from .api_views import SuscriptionAPI

urlpatterns = [
    url(r"^$", home, name="home"),
    url(r"^ingresar/$", login_register, name="login_register"),
    url(r"^mis-direcciones/$", my_address, name="my_address"),
    url(r"^mis-direcciones/(?P<pk>\d+)/$", my_address_edit, name="my_address_edit"),
    url(r"^test-email/$", test_email, name="test_email"),
    url(r"^salir/$", logout_view, name="logout_view"),
    url(r"^mi-cuenta/$", account, name="account"),
    url(r"^mis-ordenes/$", my_order, name="my_order"),
    url(r"^editar-perfil/$", edit_profle, name="edit_profle"),
    url(r"^mis-direcciones/crear/$", my_address_create, name="my_address_create"),
    url(r"^mis-ordenes/(?P<pk>\d+)/$", my_order_detail, name="my_order_detail"),
    url(r"^sigue-orden/$", follow_orders, name="follow_orders"),
    url(r"^testing_view/$", testing_view, name="testing_view"),
    url(r"^api-suscripcion/$", SuscriptionAPI.as_view(), name="api_suscripcion"),
]
