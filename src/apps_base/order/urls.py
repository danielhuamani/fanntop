from django.conf.urls import url
from rest_framework import routers
from .views import OrderViewSet

router = routers.SimpleRouter()
router.register(r'order', OrderViewSet)

urlpatterns = [
]

urlpatterns += router.urls