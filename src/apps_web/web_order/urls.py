from django.conf.urls import url
from .views import checkout_paso_1, checkout_paso_2, checkout_thanks

urlpatterns = [
    url(r"^checkout/paso-1/$", checkout_paso_1, name="checkout_paso_1"),
    url(r"^checkout/paso-2/$", checkout_paso_2, name="checkout_paso_2"),
    url(r"^checkout/gracias/$", checkout_thanks, name="checkout_thanks")
]

