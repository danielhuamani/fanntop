from django.conf.urls import url
from rest_framework import routers
from .views import (ProductClassViewSet, ProductAttributeAPI, ProductViewSet,
    ProductGaleryImageViewSet, ProductImageViewSet, ProductClassAttributeAPI)

router = routers.SimpleRouter()
router.register(r'product', ProductClassViewSet)
router.register(r'product-variant', ProductViewSet)
router.register(r'product-galery-image', ProductGaleryImageViewSet)
router.register(r'product-image', ProductImageViewSet)

urlpatterns = [
    url(r"^product-attributes/$", ProductAttributeAPI.as_view(), name="product_attributes"),
    url(r"^product-class-attributes/(?P<pk>\d+)/$", ProductClassAttributeAPI.as_view(), name="product_class_attributes")
]

urlpatterns += router.urls
