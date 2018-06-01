from django.conf.urls import url
from rest_framework import routers
from .views import (ProductClassViewSet, ProductAttributeAPI, ProductViewSet, ProductClassCreateAPI,
    ProductGaleryImageViewSet, ProductImageViewSet, ProductClassAttributeAPI, ProductClassPaso1API)

router = routers.SimpleRouter()
router.register(r'product', ProductClassViewSet)
router.register(r'product-variant', ProductViewSet)
router.register(r'product-galery-image', ProductGaleryImageViewSet)
router.register(r'product-image', ProductImageViewSet)

urlpatterns = [
    url(r"^product-paso-1/$", ProductClassPaso1API.as_view(), name="product_paso_1"),
    url(r"^product-paso-1/(?P<pk>\d+)/$", ProductClassPaso1API.as_view(), name="product_paso_1"),
    url(r"^product-create-attributes/(?P<pk>\d+)/$", ProductClassCreateAPI.as_view()),
    url(r"^product-attributes/$", ProductAttributeAPI.as_view(), name="product_attributes"),
    url(r"^product-class-attributes/(?P<pk>\d+)/$", ProductClassAttributeAPI.as_view(), name="product_class_attributes")
]

urlpatterns += router.urls
