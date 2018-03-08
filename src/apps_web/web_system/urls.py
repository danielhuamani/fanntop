from django.conf.urls import url
from .views import home, login_register, account, test_email, logout_view

urlpatterns = [
    url(r"^$", home, name="home"),
    url(r"^ingresar/$", login_register, name="login_register"),
    url(r"^mi-cuenta/$", account, name="account"),
    url(r"^test-email/$", test_email, name="test_email"),
    url(r"^salir/$", logout_view, name="logout_view"),
]

