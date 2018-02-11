from django.conf.urls import url
from rest_framework import routers
from .views import ProductClassViewSet, ProductAttributeAPI, ProductViewSet, ProductGaleryImageViewSet

router = routers.SimpleRouter()
router.register(r'product', ProductClassViewSet)
router.register(r'product-variant', ProductViewSet)
router.register(r'product-galery-image', ProductGaleryImageViewSet)

urlpatterns = [
    url(r"^product-attributes/$", ProductAttributeAPI.as_view(), name="product_attributes")
]

urlpatterns += router.urls
