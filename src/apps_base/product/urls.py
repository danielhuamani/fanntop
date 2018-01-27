from django.conf.urls import url
from rest_framework import routers
from .views import ProductClassViewSet, ProductAttributeAPI

router = routers.SimpleRouter()
router.register(r'product', ProductClassViewSet)

urlpatterns = [
    url(r"^product-attributes/$", ProductAttributeAPI.as_view(), name="product_attributes")
]

urlpatterns += router.urls
