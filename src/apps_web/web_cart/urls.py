from django.conf.urls import url
from .api_views import CartAPI
from .views import cart


urlpatterns = [
    url(r"^api/cart/$", CartAPI.as_view(), name="cart_api"),

    url(r"^carro-compras/$", cart, name="cart"),
]

