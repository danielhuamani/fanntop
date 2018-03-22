from django.conf.urls import url
from rest_framework import routers
from .views import (SuscriptionViewSet, )

router = routers.SimpleRouter()
router.register(r'suscription', SuscriptionViewSet)

urlpatterns = [
]

urlpatterns += router.urls
