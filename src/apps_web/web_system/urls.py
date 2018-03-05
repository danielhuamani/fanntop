from django.conf.urls import url
from .views import home, login_register, account

urlpatterns = [
    url(r"^$", home, name="home"),
    url(r"^ingresar/$", login_register, name="login_register"),
    url(r"^mi-cuenta/$", account, name="account"),
]

