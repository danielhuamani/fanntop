from django.conf.urls import url
from .views import checkout_paso_1, checkout_paso_2, checkout_thanks, get_price_shipping, get_coupon_discount
from .api_views import CustomerShippingAddressAPI

urlpatterns = [
    url(r"^checkout/paso-1/$", checkout_paso_1, name="checkout_paso_1"),
    url(r"^checkout/paso-2/$", checkout_paso_2, name="checkout_paso_2"),
    url(r"^checkout/gracias/$", checkout_thanks, name="checkout_thanks"),
    url(r"^ubigeo-price/$", get_price_shipping, name="get_price_shipping"),
    url(r"^validate-coupon/$", get_coupon_discount, name="get_coupon_discount"),
    url(r"^customer-shipping-address/$",
        CustomerShippingAddressAPI.as_view(),
        name="customer_shipping_address")
]

