from django.conf.urls import url
from .views import checkout_paso_1

urlpatterns = [
    url(r"^checkout/paso-1/$", checkout_paso_1, name="checkout_paso_1")
]

