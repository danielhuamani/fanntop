from django.conf.urls import url
from rest_framework import routers
from .views import ProductClassViewSet

router = routers.SimpleRouter()
router.register(r'', ProductClassViewSet)

urlpatterns = [
]

urlpatterns += router.urls