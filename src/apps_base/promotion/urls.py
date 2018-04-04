from django.conf.urls import url
from rest_framework import routers
from .views import (CouponViewSet, CouponGenerateViewSet)

router = routers.SimpleRouter()
router.register(r'coupon', CouponViewSet)
router.register(r'coupon-generate', CouponGenerateViewSet)

urlpatterns = [
]

urlpatterns += router.urls
