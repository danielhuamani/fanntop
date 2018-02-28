from django.conf.urls import url
from .api_views import CartAPI

urlpatterns = [
    url(r"^api/cart/$", CartAPI.as_view(), name="cart_api")
]

