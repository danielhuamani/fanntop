from django.conf.urls import url
from rest_framework import routers
from .views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
]

urlpatterns += router.urls