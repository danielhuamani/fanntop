from django.conf.urls import url
from rest_framework import routers
from .views import (SuscriptionViewSet, ContactViewSet, ComplaintsBookViewSet)

router = routers.SimpleRouter()
router.register(r'suscription', SuscriptionViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'complaints-book', ComplaintsBookViewSet)

urlpatterns = [
]

urlpatterns += router.urls
