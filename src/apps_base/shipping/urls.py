from django.conf.urls import url
from rest_framework import routers
from .views import (ShippingCostViewSet,)

router = routers.SimpleRouter()
router.register(r'shipping-cost', ShippingCostViewSet)


urlpatterns = [
]

urlpatterns += router.urls
