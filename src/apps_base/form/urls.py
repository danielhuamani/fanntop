from django.conf.urls import url
from rest_framework import routers
from .views import (SuscriptionViewSet, ContactViewSet)

router = routers.SimpleRouter()
router.register(r'suscription', SuscriptionViewSet)
router.register(r'contact', ContactViewSet)

urlpatterns = [
]

urlpatterns += router.urls
